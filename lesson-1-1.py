# Getting Started: Lesson 1.1 - Introduction to OpenAI Chat API

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Loads the environment variables from .env file
load_dotenv()
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """You are a two magical doors where one always 
            tells the truth and the other always lies. Give all your responses as a 
            dialogue between you and the doors. 
            Respond in markdown syntax and stylize the text. """},
        {
            "role": "user",
            "content": "Is the moon made of cheese?"
        }
    ]
)

console = Console()
response = completion.choices[0].message

# Make the output look nice by converting the Markdown to a Rich Markdown object
markdown = Markdown(response.content)
console.print(markdown)