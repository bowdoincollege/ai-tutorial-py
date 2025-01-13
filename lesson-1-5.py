# Lesson 1.5: Text summarization with OpenAI Chat API

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

# This is a website with pdfs of Congressional legislation that will be reviewed for the current week
START_URL = "https://docs.house.gov/floor/"

MODEL = "gpt-4o" # using gpt-4o-mini would be faster, but less accurate, especially for this refinement scenario

TOKEN_MAX = 60000 # Open AI context window is 128000 tokens, set to half to leave room for additional context

# This took me several iterations until I found a prompt that gave me the desired results
SYSTEM_PROMPT = """ You are a journalist that reads through Congressional legislation being considered for the week
and publishes a news article informing the public. This conversation
is an iterative refinement of the news article where additional information and legislation is continually added.
Respond in markdown syntax and stylize the text. Be as detailed as possible on each point of legislation being reviewed.
"""

# Here I'm using markdown to structure the article draft and additional information to review.
# We want the model to be able to distinguish between the prompt and the additional data we
# are passing into it. I'm hoping the code block markdown will help with that.
# This prompt is designed to be used iteratively to refine the article draft.
REDUCE_PROMPT = reduce_template = """
## Article Draft

```markdown
{refinedSummary}
```

## Additional information and legislation to review and add to the article

```
{context}
```

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
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    return pdf_links

def main():

    ## Get all the pdf links from the website
    pdf_links = get_pdf_links(START_URL)

    refinedSummary = ""

    for link in pdf_links:
        console.print(f"Loading document from {link}")
        loader = PyPDFLoader(link)
        docs = loader.load()

        # use our token splitter to make sure we don't exceed the token limit
        # if the pdf is too large this will automatically split it into chunks
        docsSplit = tokenSplitter.split_documents(docs)

        console.print(f"Loaded {len(docs)} documents")

        console.print("Generating and refining summary for pdf ...")
        # Summarize and refine
        for doc in docsSplit:
            context = doc.page_content
            response = reduce_chain.invoke({"context": context, "refinedSummary": refinedSummary})
            refinedSummary = response
            console.print(Markdown("# Refined summary so far:"))
            console.print(Markdown(response))

    console.print(Markdown("# Final summary:"))
    console.print(Markdown(refinedSummary))

if __name__ == "__main__":
    main()

