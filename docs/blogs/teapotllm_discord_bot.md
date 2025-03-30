# Building a Discord FAQ Bot with TeapotLLM

## Introduction

TeapotLLM is an open-source, hallucination-resistant language model optimized to run entirely on CPUs, making it ideal for lightweight applications. In this post, we’ll walk through building a Discord bot using TeapotLLM to answer frequently asked questions (FAQs) about the model. We’ll integrate retrieval-augmented generation (RAG) for document-based responses, utilize Brave Search for real-time context, and explore how to monitor performance using LangSmith.

## High-Level Architecture

Our bot will follow a simple workflow:

1. A user asks a question in Discord.  
2. The bot checks its stored TeapotLLM documentation for relevant answers (RAG).  
3. If needed, it queries Brave Search for additional context.  
4. The response is generated using TeapotLLM and sent back to Discord.  

### Architecture Diagram:
```
[Discord] --> [Bot Listener] --> [TeapotLLM RAG] --> [Brave Search (if needed)] --> [Response]
```

## Setting Up a Discord Bot

To get started, install the necessary dependencies:

```bash
pip install discord.py teapotai
```

### Basic Discord Bot Code

Here’s a simple Discord bot that responds with `"Hello, World!"` while ensuring it doesn’t reply to its own messages:

```python
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    async with message.channel.typing():
        await message.reply("Hello, World!")

bot.run("YOUR_DISCORD_BOT_TOKEN")
```

## Integrating TeapotLLM for FAQs

Next, we’ll use TeapotLLM to answer questions about itself. We first load relevant documentation as context.

### Loading TeapotLLM with FAQ Documents

```python
from teapotai import TeapotAI

documents = [
    "TeapotLLM is an open-source, hallucination-resistant model that runs on CPUs.",
    "TeapotLLM supports retrieval-augmented generation (RAG) for answering questions using documents.",
    "The model was trained on a synthetic dataset and optimized for efficient question answering.",
    "TeapotLLM can be hosted on low-power devices such as Raspberry Pi.",
]

teapot_ai = TeapotAI(documents=documents)
```

### Querying TeapotLLM in the Discord Bot

Modify the bot to use TeapotLLM for question answering:

```python
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    async with message.channel.typing():
        answer = teapot_ai.query(
            query=message.content,
            context=" ".join(documents)
        )
        await message.reply(answer)
```

## Integrating Brave Search for Additional Context

If TeapotLLM doesn’t have an answer, we can supplement its context with Brave Search results.

### Fetching Brave Search Results

```python
import requests

def search_brave(query):
    response = requests.get(f"https://api.search.brave.com/search?q={query}")
    return " ".join(result["snippet"] for result in response.json().get("results", []))
```

### Enhancing the Bot with Brave Search

```python
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    async with message.channel.typing():
        context = " ".join(documents)
        answer = teapot_ai.query(query=message.content, context=context)
        if "I don't have information" in answer:
            brave_context = search_brave(message.content)
            answer = teapot_ai.query(query=message.content, context=brave_context)
        await message.reply(answer)
```

## Running on a Raspberry Pi

TeapotLLM only requires ~2GB of RAM, making it suitable for lightweight devices like a Raspberry Pi. To run the bot on a Raspberry Pi:

1. Install dependencies:  
   ```bash
   pip install teapotai discord.py
   ```
2. Use a swap file if RAM is limited:  
   ```bash
   sudo fallocate -l 2G /swapfile
   ```
3. Run the bot script:  
   ```bash
   python bot.py
   ```

## Testing and Monitoring with LangSmith

### Example Test Cases

To ensure accuracy, we define test cases with expected outputs:

```python
test_cases = [
    ("What is TeapotLLM?", "TeapotLLM is an open-source, hallucination-resistant model that runs on CPUs."),
    ("Can I run TeapotLLM on Raspberry Pi?", "Yes, TeapotLLM can be hosted on low-power devices such as Raspberry Pi."),
]

def run_tests():
    for query, expected in test_cases:
        answer = teapot_ai.query(query=query, context=" ".join(documents))
        assert expected in answer, f"Test failed: {query} -> {answer}"
```

### Monitoring Performance with LangSmith

LangSmith can track latency and response accuracy.

```python
from langsmith import Client

client = Client()

def log_latency(query):
    import time
    start = time.time()
    answer = teapot_ai.query(query=query, context=" ".join(documents))
    latency = time.time() - start
    client.log_metric("latency", latency)
    return answer
```

## Conclusion

By leveraging TeapotLLM and Brave Search, we’ve built a Discord bot capable of answering FAQs efficiently while running entirely on CPUs. TeapotLLM’s low resource usage allows it to run on devices like Raspberry Pi, and with LangSmith, we can track performance and improve accuracy over time.
