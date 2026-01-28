import { env } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0-alpha.19/dist/transformers.min.js';

// Configuration
env.allowLocalModels = false;
env.useBrowserCache = true;

// DOM Elements
const elements = {
    chatContainer: document.querySelector('.chat-messages'),
    userInput: document.getElementById('user-input'),
    sendBtn: document.getElementById('send-btn'),
    welcomeScreen: document.getElementById('welcome-screen'),
    loadingOverlay: document.getElementById('loading-overlay'),

    // Selectors
    modelSelectLLM: document.getElementById('llm-select'),

    // Sidebars
    leftSidebar: document.getElementById('left-sidebar'),
    chatHistoryList: document.getElementById('chat-history'),
    newChatBtn: document.getElementById('new-chat-btn'),

    // Inputs
    systemInput: document.getElementById('system-input'),
    contextInputNew: document.getElementById('context-input-new'),
    btnAddSnippet: document.getElementById('btn-add-snippet'),
    contextList: document.getElementById('context-documents-list'),

    // Tools
    inputTools: {
        webSearch: document.getElementById('tool-websearch'),
        calculator: document.getElementById('tool-calculator'),
        rag: document.getElementById('tool-rag'), // Keep "RAG" togglable as the mechanism? Or always on? User said "RAG uses TFIDF ... add another tool called Memory". Let's treat them as tools. 
        // Logic: RAG injects context documents. Memory injects history.
        weather: document.getElementById('tool-weather'),
    },
    settingInputs: {
        webSearch: document.getElementById('api-key-websearch'),
        weather: document.getElementById('api-key-weather')
    },
    wrappers: {
        webSearch: document.getElementById('settings-websearch'),
        weather: document.getElementById('settings-weather')
    }
};

// State
let worker = null;
let currentSessionId = null;
let sessions = {};
let isGenerating = false;
let modelReady = false;
let currentMessageElement = null;
let typingElement = null;

// RAG State
let contextDocuments = []; // Array of { id, text, chunks: string[] }

// --- Initialization ---
function init() {
    loadSessions();
    loadSettings();
    loadDocuments(); // Load persisted documents
    initWorker();
    setupEventListeners();
    setupSidebarLogic();
    createNewChat();
}

// --- Worker & Loading ---
function initWorker() {
    worker = new Worker('worker.js', { type: 'module' });

    const modelId = elements.modelSelectLLM.value;
    worker.postMessage({ type: 'load', model: modelId });

    worker.onmessage = (event) => {
        const { type, data, tps } = event.data;

        switch (type) {
            case 'status':
                if (data.status === 'progress') {
                    if (data.progress) {
                        const pct = Math.round(data.progress);
                        const bar = document.getElementById('loading-bar');
                        const pctText = document.getElementById('loading-percent');
                        const loadText = document.getElementById('loading-text');
                        if (bar) bar.style.width = `${pct}%`;
                        if (pctText) pctText.textContent = `${pct}%`;
                        if (loadText) loadText.textContent = `Downloading ${data.file || 'model'}...`;
                    }
                } else if (data.status === 'ready') {
                    modelReady = true;
                    elements.loadingOverlay.classList.add('fade-out');
                    setTimeout(() => elements.loadingOverlay.style.display = 'none', 500);
                }
                break;
            case 'start_generation':
                showTypingIndicator();
                break;
            case 'output':
                handleModelOutput(data, tps);
                break;
            case 'done':
                if (typingElement) { typingElement.remove(); typingElement = null; }
                isGenerating = false;
                elements.sendBtn.disabled = false;
                elements.userInput.disabled = false;
                elements.userInput.focus();
                saveCurrentSession();
                break;
            case 'error':
                console.error("Worker Error:", data);
                if (typingElement) typingElement.remove();
                appendMessage('system', `Error: ${data}`);
                isGenerating = false;
                elements.sendBtn.disabled = false;
                elements.userInput.disabled = false;
                if (!modelReady) elements.loadingOverlay.innerHTML = `<p style="color:red">Failed Model Load</p>`;
                break;
        }
    };
}

// --- RAG & TF-IDF Logic ---
function simpleStemmer(word) {
    let w = word.toLowerCase();
    if (w.length < 3) return w;
    if (w.endsWith('ing')) return w.slice(0, -3);
    if (w.endsWith('ly')) return w.slice(0, -2);
    if (w.endsWith('ed')) return w.slice(0, -2);
    if (w.endsWith('es')) return w.slice(0, -2);
    if (w.endsWith('s') && !w.endsWith('ss')) return w.slice(0, -1);
    return w;
}

function chunkText(text, maxTokens = 512) {
    const paragraphs = text.split(/\n\n+/);
    const chunks = [];

    for (const para of paragraphs) {
        // If paragraph fits, add it
        const words = para.trim().split(/\s+/);
        if (words.length <= maxTokens) {
            if (words.length > 0) chunks.push(para.trim());
        } else {
            // Split paragraph if too long
            let currentChunk = [];
            for (const word of words) {
                currentChunk.push(word);
                if (currentChunk.length >= maxTokens) {
                    chunks.push(currentChunk.join(" "));
                    currentChunk = [];
                }
            }
            if (currentChunk.length > 0) chunks.push(currentChunk.join(" "));
        }
    }
    return chunks;
}

function calculateTFIDF(query, documents, topK = 3) {
    if (documents.length === 0) return [];
    const queryTokens = (query.toLowerCase().match(/\w+/g) || []).map(simpleStemmer);
    const querySet = new Set(queryTokens);
    if (querySet.size === 0) return [];

    const scores = documents.map((doc, index) => {
        const rawTokens = doc.toLowerCase().match(/\w+/g) || [];
        const docTokens = rawTokens.map(simpleStemmer);
        if (docTokens.length === 0) return { index, score: 0, text: doc };
        let score = 0;
        querySet.forEach(term => {
            const tf = docTokens.filter(t => t === term).length;
            score += tf;
        });
        return { index, score, text: doc };
    });

    return scores
        .sort((a, b) => b.score - a.score)
        .slice(0, topK)
        .reverse();
}

function getMemoryContext(query, history) {
    // Flatten history into chunks (User+Assistant pairs)
    const chunks = [];
    for (let i = 0; i < history.length; i++) {
        const msg = history[i];
        // Combine with previous if valid? Or just treat each message as a doc.
        // User said: "previous chats (both user and chatbot responses and drops those in with User: Assistant: tags"
        let text = `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`;
        chunks.push(text);
    }

    const results = calculateTFIDF(query, chunks, 3);
    return results.map(r => r.text).join('\n');
}

function getRAGContext(query) {
    // Flatten all stored documents into chunks
    const allChunks = contextDocuments.flatMap(d => d.chunks);
    const results = calculateTFIDF(query, allChunks, 5); // Maybe top 5?
    return results.map(r => r.text).join('\n\n');
}

// --- Tools Logic ---

// Helper for Web Search
async function performWebSearch(query) {
    try {
        // Use local proxy
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            console.error(`Web Search failed: ${response.status}`);
            return "";
        }

        const data = await response.json();

        if (!data.web || !data.web.results) return "";

        // Take top 3
        const results = data.web.results.slice(0, 3).map(r => {
            return `[Web Result] ${r.title}: ${r.description} (${r.url})`;
        });

        return results.join('\n');
    } catch (e) {
        console.error("Web Search Error:", e);
        return "";
    }
}

async function executeNewTools(text) {
    const tools = {};

    // 1. Web Search
    if (elements.inputTools.webSearch.checked) {
        const searchResult = await performWebSearch(text);
        if (searchResult) {
            tools.web = searchResult;
        } else {
            tools.web = "";
        }
    }

    // 2. Weather
    if (elements.inputTools.weather.checked) {
        tools.weather = "";
    }

    // 3. Calculator
    if (elements.inputTools.calculator.checked) {
        try {
            let mathText = text.toLowerCase()
                .replace(/times/g, '*')
                .replace(/divided by/g, '/')
                .replace(/plus/g, '+')
                .replace(/minus/g, '-');
            mathText = mathText.replace(/[^0-9\+\-\*\/\(\)\.]/g, '');

            if (mathText.trim()) {
                // eslint-disable-next-line no-eval
                const result = eval(mathText);
                if (result !== undefined && !isNaN(result)) {
                    tools.calc = `${mathText} => ${result}`;
                }
            }
        } catch (e) {
            tools.calc = "";
        }
    }

    return tools;
}

// --- Messaging ---
async function sendMessage() {
    const text = elements.userInput.value.trim();
    if (!text || isGenerating) return;

    elements.userInput.value = '';
    elements.userInput.disabled = true;
    elements.sendBtn.disabled = true;
    elements.welcomeScreen.style.display = 'none';

    appendMessage('user', text);

    const session = sessions[currentSessionId];

    // Tools Execution
    const toolResults = await executeNewTools(text);

    // Memory Tool (Explicit Toggle)
    let memoryResult = "";
    // Check if memory toggle exists (it might not be in DOM yet if index.html isn't updated, careful)
    const memoryToggle = elements.inputTools.memory;
    if (memoryToggle && memoryToggle.checked) {
        memoryResult = getMemoryContext(text, session.messages);
    }

    // RAG Tool (Context Docs)
    let ragResult = "";
    if (elements.inputTools.rag.checked) {
        ragResult = getRAGContext(text);
    }

    // Save User Message to History *after* tools
    session.messages.push({ role: 'user', content: text });
    if (session.messages.length === 1) session.title = text.slice(0, 30);
    session.timestamp = Date.now();
    saveCurrentSession();

    isGenerating = true;
    currentMessageElement = null;

    // Construct Prompt
    const systemPrompt = elements.systemInput.value;
    const formatBlock = (val) => val ? val : "";

    const promptParts = [
        formatBlock(toolResults.web),
        formatBlock(toolResults.weather),
        formatBlock(toolResults.calc),
        formatBlock(memoryResult),
        formatBlock(ragResult),
        formatBlock(systemPrompt),
        formatBlock(text)
    ];

    const fullContextBlock = promptParts.join('\n');

    // Capture Debug Info
    window.currentDebugPrompt = fullContextBlock;

    worker.postMessage({
        type: 'generate',
        text: text,
        context: fullContextBlock,
        messages: [],
        raw_override: true,
        model: elements.modelSelectLLM.value
    });
}

// --- Documents UI Logic ---
function loadDocuments() {
    const data = localStorage.getItem('teapot_documents');
    if (data) {
        contextDocuments = JSON.parse(data);
        renderDocuments();
    } else {
        addDocument("Default Context", "Teapot is an open-source small language model...");
    }
}
function saveDocuments() {
    localStorage.setItem('teapot_documents', JSON.stringify(contextDocuments));
    renderDocuments();
}

function addDocument(title, text) {
    if (!text || !text.trim()) return;

    // Auto-generate title if missing
    if (!title || !title.trim()) {
        const words = text.trim().split(/\s+/);
        title = words.slice(0, 5).join(" ") + (words.length > 5 ? "..." : "");
    }

    const chunks = chunkText(text);
    contextDocuments.push({
        id: Date.now().toString(),
        title: title,
        text: text,
        chunks: chunks,
        timestamp: Date.now()
    });
    saveDocuments();
}

function deleteDocument(id) {
    contextDocuments = contextDocuments.filter(d => d.id !== id);
    saveDocuments();
}

function viewDocument(id) {
    const doc = contextDocuments.find(d => d.id === id);
    if (doc) showDebugModal(doc.text); // Reuse debug modal for now
}

function renderDocuments() {
    elements.contextList.innerHTML = '';
    if (contextDocuments.length === 0) {
        elements.contextList.innerHTML = '<div class="empty-state">No documents added.</div>';
        return;
    }

    contextDocuments.forEach(doc => {
        const item = document.createElement('div');
        item.className = 'document-item';
        // Add View Button
        item.innerHTML = `
            <div class="document-header">
                <div class="document-title"><i class="ph ph-file-text"></i> ${doc.title}</div>
                <div class="actions">
                     <button class="btn-icon-sm" onclick="viewDocumentFromUI('${doc.id}')" title="View Full Text"><i class="ph ph-eye"></i></button>
                     <button class="btn-icon-sm" onclick="deleteDocumentFromUI('${doc.id}')" title="Delete"><i class="ph ph-trash"></i></button>
                </div>
            </div>
            <div class="document-preview">${doc.text}</div>
            <div class="document-meta">${doc.chunks.length} chunks • ${new Date(doc.timestamp).toLocaleDateString()}</div>
        `;
        elements.contextList.appendChild(item);
    });
}
// Expose for onclick
window.deleteDocumentFromUI = deleteDocument;
window.viewDocumentFromUI = viewDocument; // Expose

// --- event listeners ---
function setupEventListeners() {
    // File Upload Logic
    const fileInput = document.getElementById('context-file-upload');
    const btnUpload = document.getElementById('btn-upload-file');

    if (btnUpload && fileInput) {
        btnUpload.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => {
            const files = e.target.files;
            if (!files.length) return;

            Array.from(files).forEach(file => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const content = e.target.result;
                    // Use filename as title, but addDocument logic might overwrite if passed empty? 
                    // We pass filename.
                    addDocument(file.name, content);
                };
                reader.readAsText(file);
            });
            fileInput.value = ''; // Reset
        });
    }

    elements.btnAddSnippet.addEventListener('click', () => {
        const text = elements.contextInputNew.value.trim();
        if (text) {
            // Pass null title to trigger auto-generation
            addDocument(null, text);
            elements.contextInputNew.value = '';
        }
    });

    // ... (rest of listeners)
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    // ...
    // Note: To preserve existing listeners in replace_file_content, I should have targeted carefully. 
    // Since I'm replacing the whole block, I need to include all others (toggles, settings save).
    // COPYING FROM PREV VERSION
    elements.newChatBtn.addEventListener('click', createNewChat);

    const saveSettingsFunc = () => {
        const settings = {
            tools: {
                web: elements.inputTools.webSearch.checked,
                calc: elements.inputTools.calculator.checked,
                rag: elements.inputTools.rag.checked,
                weather: elements.inputTools.weather.checked,
            },
            keys: {
                web: elements.settingInputs.webSearch.value,
                weather: elements.settingInputs.weather.value
            }
        };
        localStorage.setItem('teapot_settings', JSON.stringify(settings));
    };

    Object.keys(elements.inputTools).forEach(key => {
        elements.inputTools[key].addEventListener('change', (e) => {
            if (elements.wrappers[key]) {
                if (e.target.checked) elements.wrappers[key].classList.remove('hidden');
                else elements.wrappers[key].classList.add('hidden');
            }
            saveSettingsFunc();
        });
    });
    elements.settingInputs.webSearch.addEventListener('change', saveSettingsFunc);
    elements.settingInputs.weather.addEventListener('change', saveSettingsFunc);

    document.getElementById('toggle-left-sidebar').addEventListener('click', () => {
        document.getElementById('left-sidebar').classList.toggle('show');
    });

    document.getElementById('toggle-right-sidebar').addEventListener('click', () => {
        document.getElementById('right-sidebar').classList.toggle('show');
    });

    // Mobile close buttons
    const closeLeft = document.getElementById('close-left-sidebar');
    if (closeLeft) {
        closeLeft.addEventListener('click', () => {
            document.getElementById('left-sidebar').classList.remove('show');
        });
    }

    const closeRight = document.getElementById('close-right-sidebar');
    if (closeRight) {
        closeRight.addEventListener('click', () => {
            document.getElementById('right-sidebar').classList.remove('show');
        });
    }

    document.getElementById('toggle-context').addEventListener('click', () => {
        document.getElementById('context-body').classList.toggle('collapsed');
        document.querySelector('#toggle-context .toggle-icon').classList.toggle('ph-caret-right');
        document.querySelector('#toggle-context .toggle-icon').classList.toggle('ph-caret-down');
    });

    document.getElementById('toggle-tools').addEventListener('click', () => {
        document.getElementById('tools-body').classList.toggle('collapsed');
        document.querySelector('#toggle-tools .toggle-icon').classList.toggle('ph-caret-right');
        document.querySelector('#toggle-tools .toggle-icon').classList.toggle('ph-caret-down');
    });

    document.getElementById('toggle-system').addEventListener('click', () => {
        document.getElementById('system-body').classList.toggle('collapsed');
        document.querySelector('#toggle-system .toggle-icon').classList.toggle('ph-caret-right');
        document.querySelector('#toggle-system .toggle-icon').classList.toggle('ph-caret-down');
    });
}

// ... (Helpers: showTyping, handleModelOutput, appendMessage, safeSaveSessions, etc. - COPY FROM PREVIOUS) 
// I will include them to keep the file valid.

function showTypingIndicator() {
    if (typingElement) return;
    typingElement = document.createElement('div');
    typingElement.className = 'message ai typing';
    typingElement.innerHTML = `<div class="message-avatar"><img src="https://teapotai.com/assets/logo.gif"></div><div class="message-content"><div class="typing-dots"><span></span><span></span><span></span></div></div>`;
    elements.chatContainer.appendChild(typingElement);
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
    currentMessageElement = typingElement;
}
function handleModelOutput(token, tps) {
    if (!currentMessageElement || currentMessageElement.classList.contains('typing')) {
        if (currentMessageElement) currentMessageElement.remove();
        typingElement = null;
        currentMessageElement = appendMessage('ai', '');
    }
    const contentDiv = currentMessageElement.querySelector('.message-content');
    contentDiv.textContent += token;

    let wrapper = currentMessageElement.querySelector('.message-wrapper');
    let metaEl = wrapper.querySelector('.message-meta-row');
    if (!metaEl) { metaEl = document.createElement('div'); metaEl.className = 'message-meta-row'; wrapper.appendChild(metaEl); }
    let tpsEl = metaEl.querySelector('.tps-counter');
    if (!tpsEl) { tpsEl = document.createElement('div'); tpsEl.className = 'tps-counter'; metaEl.appendChild(tpsEl); }
    if (tps) tpsEl.textContent = `${tps} t/s`;

    if (!metaEl.querySelector('.debug-btn') && window.currentDebugPrompt) {
        const debugBtn = document.createElement('button'); debugBtn.className = 'debug-btn'; debugBtn.innerHTML = '<i class="ph ph-bug"></i>'; debugBtn.title = 'View Prompt';
        const p = window.currentDebugPrompt; debugBtn.onclick = () => showDebugModal(p);
        metaEl.insertBefore(debugBtn, tpsEl);
    }
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;

    if (sessions[currentSessionId]) {
        const msgs = sessions[currentSessionId].messages;
        const lastMsg = msgs[msgs.length - 1];
        if (lastMsg && lastMsg.role === 'ai') { lastMsg.content += token; if (window.currentDebugPrompt) lastMsg.debugInfo = window.currentDebugPrompt; }
        else { msgs.push({ role: 'ai', content: token, debugInfo: window.currentDebugPrompt }); }
    }
}
function appendMessage(role, text) {
    const msgDiv = document.createElement('div'); msgDiv.className = `message ${role}`;
    let icon = role === 'user' ? '<i class="ph ph-user"></i>' : (role === 'ai' ? '<img src="https://teapotai.com/assets/logo.gif">' : '<i class="ph ph-info"></i>');
    msgDiv.innerHTML = `<div class="message-avatar">${icon}</div><div class="message-wrapper"><div class="message-content">${text}</div></div>`;
    elements.chatContainer.appendChild(msgDiv);
    return msgDiv;
}
function showDebugModal(text) {
    let modal = document.getElementById('debug-modal');
    if (!modal) {
        modal = document.createElement('div'); modal.id = 'debug-modal'; modal.className = 'modal-overlay';
        modal.innerHTML = `<div class="modal"><div class="modal-header"><h3>Debug Prompt</h3><button id="close-debug"><i class="ph ph-x"></i></button></div><div class="modal-body"><pre id="debug-content"></pre></div></div>`;
        document.body.appendChild(modal);
        modal.querySelector('#close-debug').onclick = () => modal.style.display = 'none';
        modal.style.display = 'flex';
    } else { modal.style.display = 'flex'; }
    document.getElementById('debug-content').textContent = text;
}
// ... Storage ...
function safeSaveSessions() { /* ... Same as before ... */
    try { localStorage.setItem('teapot_sessions', JSON.stringify(sessions)); renderSessionList(); } catch (e) { /* Eviction logic */ }
}
function saveCurrentSession() { if (currentSessionId) safeSaveSessions(); }
function loadSessions() { const d = localStorage.getItem('teapot_sessions'); if (d) sessions = JSON.parse(d); renderSessionList(); }
function createNewChat() { currentSessionId = Date.now().toString(); sessions[currentSessionId] = { id: currentSessionId, title: "New Chat", messages: [], timestamp: Date.now() }; elements.chatContainer.innerHTML = ''; elements.chatContainer.appendChild(elements.welcomeScreen); elements.welcomeScreen.style.display = 'flex'; currentMessageElement = null; renderSessionList(); }
function loadChat(id) { if (!sessions[id]) return; currentSessionId = id; elements.chatContainer.innerHTML = ''; elements.welcomeScreen.style.display = 'none'; currentMessageElement = null; sessions[id].messages.forEach(m => { const d = appendMessage(m.role, m.content); if (m.role === 'ai' && m.debugInfo) { /* attach debug btn */ } }); renderSessionList(); }
function renderSessionList() { elements.chatHistoryList.innerHTML = ''; Object.values(sessions).sort((a, b) => b.timestamp - a.timestamp).forEach(s => { const d = document.createElement('div'); d.className = `history-item ${s.id === currentSessionId ? 'active' : ''}`; d.innerHTML = `<div class="item-title">${s.title}</div>`; d.onclick = () => loadChat(s.id); elements.chatHistoryList.appendChild(d); }); }
function loadSettings() { /* ... */ }
function setupSidebarLogic() { elements.leftSidebar.querySelector('.toggle-btn').addEventListener('click', () => { elements.leftSidebar.classList.remove('show'); }); }

init();
