# Lesson 1.2: Add User Input to Chat API

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
client = OpenAI()

console = Console()

# Loop to keep the conversation going, type "exit" or "quit" to stop
while True:
    user_input = console.input("[bold green]You:[/bold green] ")

    if user_input.lower() in ["exit", "quit"]:
        break

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a two magical doors where one always 
                tells the truth and the other always lies. Give all your responses as a 
                dialogue between you and the doors. 
                Respond in markdown syntax and stylize the text. """},
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    response = completion.choices[0].message
    markdown = Markdown(response.content)
    console.print(markdown)