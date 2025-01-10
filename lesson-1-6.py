# Lesson 1.6: Vision (multi-modal) with OpenAI

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from PIL import Image
import base64
from io import BytesIO

MODEL = "gpt-4o"

load_dotenv()
client = OpenAI()

console = Console()

# Keep track of the chat history in an array
chat_history = []

# Load the image and encode it in base64
image_path = "us-national-archive-sample.jpg"
with open(image_path, "rb") as image_file:
    image = Image.open(image_file)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

# Enter the game loop!
while True:
    user_input = console.input("[bold green]You:[/bold green] ")

    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history.append({"role": "user", "content": user_input})

    messages = [
        {"role": "system", "content": """You are a helpful assistant. 
         Respond in markdown syntax and stylize the text. """},
        {"role": "user", "content": [
                {"type": "text", "text": "Use this image to answer the following questions."},
                {
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64})"}
                }
            ]}
    ] + chat_history

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    response = completion.choices[0].message.content
    console.print(Markdown(response))
    chat_history.append({"role": "assistant", "content": response})