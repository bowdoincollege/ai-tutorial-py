# Generative AI: Getting Started

Pre-requisites

* A computer
* Open AI API Key
* Python 3+ installed
* Pip3 (usually included with Python install)
* Git
* Clone this repository

Recommended

* Visual Studio Code IDE

## Setup

Managing dependencies in Python

```sh
cd Getting_Started

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r requirements.txt
```

* Copy the .env.example file to .env and fill out the environment variables

## Lesson 1: Getting Started!

Making the very basic 'hello world' call to the OpenAI API.

[lesson-1-1.py](lesson-1-1.py)

## Lesson 2: Chat

Accepting basic user input.

[lesson-1-2.py](lesson-1-2.py)

## Lesson 3: Chat memory

Adding context so that the chat bot remembers the conversation.

[lesson-1-3.py](lesson-1-3.py)

## Lesson 4: Visualizations

Taking advantage of Markdown syntax to improve the output formatting

[lesson-1-4.py](lesson-1-4.py)

## Lesson 5: Summarization

Taking things up a notch. Adding code to scrape the web and generating a summary of
text that exceeds the context window of the LLM (128,000 tokens for OpenAI models).
This is often referred to as RAG: Retrieval-Augmented Generation, supplementing data
from an external source from the LLM training data.

[lesson-1-5.py](lesson-1-5.py)

## References

* https://realpython.com/python-rich-package/
* https://platform.openai.com/docs/quickstart?language-preference=python&quickstart-example=completions
* https://python.langchain.com/docs/tutorials/summarization/#map-reduce