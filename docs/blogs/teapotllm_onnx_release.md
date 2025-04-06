# Running TeapotLLM in the Browser- ONNX Release

## Introduction

[TeapotLLM](https://huggingface.co/teapotai/teapotllm) is an open-source, hallucination-resistant language model designed to run entirely on CPUs, making it ideal for building lightweight and cost-effective chatbot applications.

We’ve now added support for loading TeapotLLM directly in the browser using [Transformers.js](https://huggingface.co/docs/transformers.js/en/index). This opens up new possibilities for running LLMs on any end-user device—no server required.

![https://teapotai.com/assets/toaster.png](https://teapotai.com/assets/toaster.png)

## Library Support

We’re actively working on an npm package that brings TeapotLLM to the browser. The library will include all the key features of the Python version—like retrieval-augmented generation (RAG), intelligent context chunking, prompt formatting, and answer extraction. Our goal is to have feature parity between both ecosystems and continue to ship enhancements to all environments so that you can deploy teapotllm wherever makes the most sense for your use case.

## Demo 
We have a demo on our website that you can try out [here](https://teapotai.com/playground).

![https://teapotai.com/assets/webdemo.png](https://teapotai.com/assets/webdemo.png)



## Using Transformers.js

You can already try out TeapotLLM in your browser using [Transformers.js](https://huggingface.co/docs/transformers.js/en/index). Just use the `pipeline` function to load the model from the Hugging Face Hub:

```js
import { pipeline } from '@xenova/transformers';

const generate = await pipeline('text2text-generation', 'teapotai/teapotllm');

// Run inference
const context = "The Eiffel Tower is a wrought iron lattice tower in Paris, France. It was designed by Gustave Eiffel and completed in 1889."
const query = "What is the height of the Eiffel Tower?"
const result = await generate(context+"\n"+query);
console.log(result[0].generated_text);  // → "The Eiffel Tower stands at a height of 330 meters."
```

No GPU or server needed—everything runs right in the browser using ONNX under the hood.

## Community

A huge thanks to the community members who contributed to the ONNX conversion and helped test the web demo. Your support has been critical in making TeapotLLM more accessible, and we’re grateful for our amazing community collaboration and feedback.

## Conclusion

Our goal is to make TeapotLLM run everywhere—from laptops and smartphones to edge servers. If you’re curious, building something, or just want to say hi, join us on [Discord](https://discord.com/invite/hPxGSn5dST)!



