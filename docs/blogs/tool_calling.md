# Teapotllm Tools- a <1b parameter model with tool calling

## Why build a 1b parameter Tool calling LLM?
We have built a fast, hallucination resistant model called TeapotLLM that can run on low-end devices such as CPUs. The ability to detect if the provided context contains the required information to answer a user query is instrumental in being able to detect how to appropriately use tools . We show here that the hallucination resistance of TeapotLLM allows it , which are traditioanlly reserved for SOTA closed source models or models with 10-100b+ parameters.

## Try it out
If you want to come check out Teapotllm's capabilities, visit our Discord.

We also have a python library on our website to help you easily set up RAG & Tool use applications locally.

## Requirements
- We wanted users to be able specify arbitrary tools and arguments to fit a variety of use cases
- we wanted to ensure that these queries were well typed and conform to a schema
- We wanted to build a tool calling framework that worked with our existing teapotllm model without further fine-tuning to avoid task bias



## Building a Tool Calling Model 
We built a tool calling library levearging o
1. We first ask our model to answer the question with the existing context
2. If we detect a refusal (ie it is unable to answer), then we attempt to select a tool
3. Once a valid tool has been selected, we then indepdently parese each argument using our model
4. We then pass the arguments to the tool and then return the tools response as context to a new query to the LLM



![[https://teapotai.com/assets/teapottools_flow.png](https://teapotai.com/assets/teapottools_flow_notools.png)

![https://teapotai.com/assets/teapottools_flow.png](https://teapotai.com/assets/teapottools_flow.png)




## Evaluations
We built a small dataset of tool calling examples to test TeapotLLM against similarly sized models. Our findings show that Teapotllm significantly outperforms models in a similar size range and approaches the performance of SOTA models on simple tool calling tasks, such as GPT-4 (we did not include closed source models on this graph but did extensively test and they received perfect accuracy on our eval set).

Teapotllm is able to accurately extract arguments without hallucinating from messages.

![http://teapotai.com/assets/tool_argument_eval.jpg](http://teapotai.com/assets/tool_argument_eval.jpg)

![https://teapotai.com/assets/tool_selection_eval.jpg](https://teapotai.com/assets/tool_selection_eval.jpg)
