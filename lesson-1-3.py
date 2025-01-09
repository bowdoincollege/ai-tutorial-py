# Lesson 1.3: Add Chat memory to Chat API and count tokens

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
import tiktoken

MODEL = "gpt-4o"

load_dotenv()
client = OpenAI()

console = Console()

# Keep track of the chat history in an array
chat_history = []

# TikToken is a library that helps with tokenizing text for OpenAI models, great for counting tokens
enc = tiktoken.encoding_for_model(MODEL)

# Enter the game loop!
while True:
    user_input = console.input("[bold green]You:[/bold green] ")

    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history.append({"role": "user", "content": user_input})

    messages = [
        {"role": "system", "content": """You are a two magical doors where one always 
            tells the truth and the other always lies. Give all your responses as a 
            dialogue. Respond in markdown syntax and stylize the text. """}
    ] + chat_history

    # Calculate the total number of tokens, this is helpful for staying within the token limit
    # of the context window of the OpenAI model
    total_tokens = sum(len(enc.encode(message["content"])) for message in messages)
    console.print(f"[bold blue]Total tokens:[/bold blue] {total_tokens}")

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    assistant_response = completion.choices[0].message.content
    console.print(Markdown(assistant_response))

    # include the assistant response in the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})