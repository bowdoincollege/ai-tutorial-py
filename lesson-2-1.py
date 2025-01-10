# Lesson 2.1: Getting started with Ollama and local models

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

MODEL = "llama3.2"

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
client = OllamaLLM(model=MODEL)

console = Console()
chat_history = []
chat_history.append(SystemMessage(content=SYSTEM_PROMPT))

while True:
    user_input = console.input("[bold green]You:[/bold green] ")

    if user_input.lower() in ["exit", "quit"]:
        break

    # Process user input as usual
    humanMessage = HumanMessage(content=user_input)
    chat_history.append(humanMessage)

    completion = client.invoke(chat_history)

    chat_history.append(AIMessage(completion))
    assistant_response = completion

    console.print(Markdown(assistant_response))
