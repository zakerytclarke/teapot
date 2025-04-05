# Teapot LLM Changelog 1.1.0
We've updated the library with some exciting new features in teapotai@1.0.1!

## Automatic Context Chunking
You can now pass in arbitrary sized documents and the library will automatically chunk them to fit in the models context:
```python
from teapotai import TeapotAI
import requests

washington_context = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=true&titles=George_Washington").json()['query']['pages'].popitem()[1]['extract']
adams_context = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=true&titles=John_Adams").json()['query']['pages'].popitem()[1]['extract']
jefferson_context = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=true&titles=Thomas_Jefferson").json()['query']['pages'].popitem()[1]['extract']


# Load in entire wikipedia pages 
teapot_ai = TeapotAI(
    documents=[washington_context, adams_context, jefferson_context]
)

teapot_ai.query("Tell me about george washington")
```


## Custom Models & Tokenizers
We've also added the ability to pass in your own custom model & tokenizer that leverage the teapot library.
```python
from teapotai import TeapotAI
from transformers import AutoTokenizer, AutoModelForCausalLM


teapot_ai = TeapotAI(
    model=AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct"),
    tokenizer=AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct"),
)

teapot_ai.query("who are you?")
```