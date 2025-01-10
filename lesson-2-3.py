# Lesson 2.3: Vision (multi-modal) with Ollama

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import base64
import ollama

# In your Terminal app, if you haven't already, run (keep an eye on your hard drive space!): ollama pull llama3.2-vision
MODEL = "llama3.2-vision"

load_dotenv()
console = Console()

# load sample png image screenshot-code.png as base64
with open("screenshot-code.png", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

    response = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": "Describe the image and tell me what the code does.",
            "images": [f"{image_data}"],
        }],
    )

    console.print(Markdown(response['message']['content']))