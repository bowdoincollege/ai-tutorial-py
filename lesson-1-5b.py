# Lesson 1.5b: Text summarization with OpenAI Chat API

# the Langchain library includes a ChatOpenAI class that wraps the OpenAI API and provides additional functionality
# it's a great library for working with other LLM models and has lots of out of the box
# functionality for working with data

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from langchain_openai import ChatOpenAI
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import TokenTextSplitter
from urllib.parse import urljoin
import os

# This is a website with pdfs of Supreme Court oral arguments
START_URL = "https://www.supremecourt.gov/oral_arguments/argument_transcript/2024"

MODEL = "gpt-4o" # using gpt-4o-mini would be faster, but less accurate, especially for this refinement scenario

TOKEN_MAX = 60000 # Open AI context window is 128000 tokens, set to half to leave room for additional context

# This took me several iterations until I found a prompt that gave me the desired results
SYSTEM_PROMPT = """ You are a journalist that reads through Supreme Court oral arguments. This conversation
is an iterative refinement of the news article where additional information and oral arguments are continually added.
Respond in markdown syntax and stylize the text. Be as detailed as possible on each case being reviewed and 
make judgements on how the court might decide based on the questions, responses, and behavior of the justices 
toward each side. Ignore the appendix and index pages at the end of each of the argument transcripts.
"""

# Here I'm using markdown to structure the article draft and additional information to review.
# We want the model to be able to distinguish between the prompt and the additional data we
# are passing into it. I'm hoping the code block markdown will help with that.
# This prompt is designed to be used iteratively to refine the article draft.
REDUCE_PROMPT = reduce_template = """
## Article Draft

{refinedSummary}

## Additional information and/or cases to review and add to the article

{context}

"""

load_dotenv()
llm = ChatOpenAI(model=MODEL)

# The chat prompt template is a reusable way to structure the conversation with the model
reduce_prompt = ChatPromptTemplate([("system", SYSTEM_PROMPT),("human", REDUCE_PROMPT)])
reduce_chain = reduce_prompt | llm | StrOutputParser()

# TokenTextSplitter is a utility to split text into chunks of a certain size,
# in this case we are splitting the text into chunks based on a max token size
tokenSplitter = TokenTextSplitter(chunk_size=TOKEN_MAX, chunk_overlap=0, model_name=MODEL)

console = Console()

# Function to get all the pdf links from a given url, let's us crawl the site for pdfs
def get_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # handle relative links, e.g. ../../pdf/2024/202
    pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    # filter pdf links where the file name starts with 23- or 24-
    # to avoid non oral argument pdfs
    filtered_pdf_links = [link for link in pdf_links if os.path.basename(link).startswith(('23-', '24-'))]
    return filtered_pdf_links

def load_and_process_pdf(link):
    loader = PyPDFLoader(link)
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])

    # Split the text at "The case is submitted" and take the part before it
    # These transcripts have a lot of extra information at the end that we don't need
    # and also create a lot of extra tokens
    split_text = text.split("The case is submitted")[0]
    return split_text

def main():

    ## Get all the pdf links from the website
    pdf_links = get_pdf_links(START_URL)

    refinedSummary = ""

    for link in pdf_links:
        console.print(f"Loading document from {link}")
        loader = PyPDFLoader(link)

        processed_text = load_and_process_pdf(link)

        # use our token splitter to make sure we don't exceed the token limit
        # if the pdf is too large this will automatically split it into chunks
        strSplit = tokenSplitter.split_text(processed_text)

        console.print("Generating and refining summary for pdf ...")
        # Summarize and refine
        for str in strSplit:
            context = str
            response = reduce_chain.invoke({"context": context, "refinedSummary": refinedSummary})
            refinedSummary = response
            console.print(Markdown("# Refined summary so far:"))
            console.print(Markdown(response))

    console.print(Markdown("# Final summary:"))
    console.print(Markdown(refinedSummary))

if __name__ == "__main__":
    main()

