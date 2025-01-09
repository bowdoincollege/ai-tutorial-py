# Lesson 1.4: Visualizations with OpenAI Chat API

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
import tiktoken

MODEL = "gpt-4o"

# Let's refine the system prompt to add tables and ASCII art
SYSTEM_PROMPT = """You are a two magical doors where one always
tells the truth and the other always lies. Do not give away which is which. 
Give all your responses as a dialogue. Never break character.

* Respond in markdown syntax and stylize the text.
* Put tabular data in a markdown table.
* Render any visualizations as ASCII art.

Response:

"""

load_dotenv()
client = OpenAI()

console = Console()
chat_history = []

enc = tiktoken.encoding_for_model(MODEL)

while True:
    user_input = console.input("[bold green]You:[/bold green] ")

    if user_input.lower() in ["exit", "quit"]:
        break

    # Process user input as usual
    chat_history.append({"role": "user", "content": user_input})

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + chat_history

    # Calculate the total number of tokens
    total_tokens = sum(len(enc.encode(message["content"])) for message in messages)
    console.print(f"[bold blue]Total tokens:[/bold blue] {total_tokens}")

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    assistant_response = completion.choices[0].message.content

    console.print(Markdown(assistant_response))
    chat_history.append({"role": "assistant", "content": assistant_response})
