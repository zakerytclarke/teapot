import { pipeline, env, TextStreamer } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0-alpha.19/dist/transformers.min.js';

// Configuration
env.allowLocalModels = false;
env.useBrowserCache = true;

// Singleton to hold the pipeline
class TextGenerationPipeline {
    static task = 'text2text-generation'; // T5 is seq2seq, user confirmed teapotllm fits this
    static model = 'teapotai/teapotllm';
    static instance = null;

    static async getInstance(modelId, progressCallback = null) {
        // Direct usage of requested models
        let targetModel = modelId;

        if (this.instance === null || this.model !== targetModel) {
            this.model = targetModel;
            self.postMessage({ type: 'status', data: { status: 'loading', model: targetModel } });


            try {
                this.instance = await pipeline(this.task, this.model, {
                    progress_callback: (data) => {
                        // transformers.js v2 sends { status: 'progress', loaded: X, total: Y, name: Z }
                        if (data.status === 'progress') {
                            const pct = (data.loaded / data.total) * 100;
                            if (progressCallback) progressCallback({
                                status: 'progress',
                                progress: pct,
                                file: data.file
                            });
                        }
                    }
                });
                self.postMessage({ type: 'status', data: { status: 'ready', model: targetModel } });
            } catch (err) {
                console.error("Failed to load model:", err);
                // Fallback attempt?
                self.postMessage({ type: 'error', data: `Failed to load ${targetModel}: ${err.message}` });
                throw err;
            }
        }
        return this.instance;
    }
}

// Message Handler
self.addEventListener('message', async (event) => {
    const { type, text, messages, model, context } = event.data;

    if (type === 'load') {
        try {
            await TextGenerationPipeline.getInstance(model, (data) => {
                self.postMessage({ type: 'status', data: data });
            });
        } catch (err) {
            // Error handled in getInstance
        }
        return;
    }

    if (type === 'generate') {
        let generator;
        try {
            generator = await TextGenerationPipeline.getInstance(model);
        } catch (err) {
            self.postMessage({ type: 'error', data: err.message });
            return;
        }

        let prompt;
        // Check for raw override (provided via context by app.js logic)
        // If messages is empty and context is provided with raw_override intention
        if (event.data.raw_override) {
            prompt = context; // The full constructed prompt
            // Append "Assistant:" if not present at end? 
            // User prompt construction ended with "{question}". 
            // Usually we need to prompt the model to answer. 
            // "Teapot is ... {question}" -> Model might just continue text.
            // Standard practice is "Question: ... Answer:" or similar.
            // The user's prompt format didn't specify an "Answer:" suffix.
            // "We then concatenate all of those into the format of f'...{question}'"
            // I will assume the model is smart enough or the user wants exactly that.
            // But for safety with T5, we usually need an indicator.
            // However, I will strictly follow "format of ... {question}".
        } else {
            // Fallback to standard chat template
            prompt = "";
            if (context) {
                prompt += `System: Use the following context to answer the user request:\n${context}\n\n`;
            }
            messages.forEach(msg => {
                if (msg.role === 'user') prompt += `User: ${msg.content}\n`;
                else if (msg.role === 'ai') prompt += `Assistant: ${msg.content}\n`;
            });
            prompt += `Assistant:`;
        }

        const startTime = performance.now();
        let tokenCount = 0;

        try {
            // v3 Streaming
            const streamer = new TextStreamer(generator.tokenizer, {
                skip_prompt: true,
                callback_function: (text) => {
                    tokenCount++;
                    const elapsed = (performance.now() - startTime) / 1000;
                    const tps = (tokenCount / elapsed).toFixed(2);

                    self.postMessage({
                        type: 'output',
                        data: text,
                        tps: tps
                    });
                }
            });

            self.postMessage({ type: 'start_generation' });

            const output = await generator(prompt, {
                max_new_tokens: 512,
                temperature: 0.7,
                do_sample: true,
                streamer: streamer,
            });

        } catch (err) {
            self.postMessage({ type: 'error', data: err.message });
        }

        self.postMessage({ type: 'done' });
    }
});
