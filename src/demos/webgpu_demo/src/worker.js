import { pipeline, TextStreamer, StoppingCriteria } from '@huggingface/transformers';

class CallbackTextStreamer extends TextStreamer {
    constructor(tokenizer, cb) {
        super(tokenizer, {
            skip_prompt: true,
            skip_special_tokens: true,
        });
        this.cb = cb;
    }

    on_finalized_text(text) {
        this.cb(text);
    }
}

class InterruptableStoppingCriteria extends StoppingCriteria {
    constructor() {
        super();
        this.interrupted = false;
    }

    interrupt() {
        this.interrupted = true;
    }

    reset() {
        this.interrupted = false;
    }

    _call(input_ids) {
        return new Array(input_ids.length).fill(this.interrupted);
    }
}

const stopping_criteria = new InterruptableStoppingCriteria();

class TeapotAIPipeline {
    static instance = null;

    constructor() {
        this.modelId = 'teapotai/teapotllm';
        this.generator = null;
    }

    static getInstance() {
        if (!TeapotAIPipeline.instance) {
            TeapotAIPipeline.instance = new TeapotAIPipeline();
        }
        return TeapotAIPipeline.instance;
    }

    async initialize(progress_callback = null) {
        if (this.generator) return this.generator;

        this.generator = await pipeline('text2text-generation', this.modelId, {
            dtype: 'q4',
            device: 'webgpu',
            progress_callback,
        });

        return this.generator;
    }
}

async function generate(messages) {
    const generator = await TeapotAIPipeline.getInstance().initialize();

    let startTime;
    let numTokens = 0;
    const cb = (output) => {
        startTime ??= performance.now();

        let tps;
        if (numTokens++ > 0) {
            tps = numTokens / (performance.now() - startTime) * 1000;
        }
        self.postMessage({
            status: 'update',
            output, tps, numTokens,
        });
    }

    const streamer = new CallbackTextStreamer(generator.tokenizer, cb);

    // Tell the main thread we are starting
    self.postMessage({ status: 'start' });

    // Format messages into a single string handling both content and context
    // const formattedMessages = messages.map(m => {
    //     let messageText = '';
    //     if (m.context) {
    //         messageText += `Context: ${m.context}\n`;
    //     }
    //     messageText += m.content;
    //     return messageText;
    // }).join('\n');
    // console.log(messages)

    // const input = formattedMessages + '\nagent:';
    const input  = messages.slice(-1)[0].context+"\n"+messages.slice(-1)[0].content;
    console.log(input)
    const output = await generator(input, {
        max_new_tokens: 512,
        streamer,
        stopping_criteria,
    });

    // Send the output back to the main thread
    self.postMessage({
        status: 'complete',
        output: output[0].generated_text,
    });
}

async function load() {
    self.postMessage({
        status: 'loading',
        data: 'Loading model...'
    });

    const generator = await TeapotAIPipeline.getInstance().initialize(x => {
        self.postMessage(x);
    });

    self.postMessage({
        status: 'loading',
        data: 'Compiling shaders and warming up model...'
    });

    // Run model with dummy input to compile shaders
    await generator('a', { max_new_tokens: 1 });
    self.postMessage({ status: 'ready' });
}

// Listen for messages from the main thread
self.addEventListener('message', async (e) => {
    const { type, data } = e.data;

    switch (type) {
        case 'load':
            load();
            break;

        case 'generate':
            stopping_criteria.reset();
            generate(data);
            break;

        case 'interrupt':
            stopping_criteria.interrupt();
            break;

        case 'reset':
            stopping_criteria.reset();
            break;
    }
});