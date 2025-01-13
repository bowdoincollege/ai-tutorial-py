# Lesson 1.7: Using OpenAI with Flask to create a dynamic web application
#
# To start, run this in the terminal: flask --app lesson-1-7 run
# Use the url provided, including the port number, 
# to view the web application (e.g. http://127.0.0.1:5000)

from flask import Flask
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
client = OpenAI()

app = Flask(__name__)

@app.route("/")
def hello_world():
    messages = [
        {"role": "system", "content": """You are a web server that returns a single
            standalone html file based on the user's request. Include vanilla embedded javascript and CSS.
            Make the html page interactive and responsive and pretty. All of the page should be
            in a single Markdown code block. """},
        {"role": "user", "content": """
        Create a single player game of pong. Include instructions on how to play.
                     """}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    markdown_content = completion.choices[0].message.content

    # Extract HTML from markdown code block
    html_content = re.search(r'```html(.*?)```', markdown_content, re.DOTALL).group(1).strip()

    return html_content