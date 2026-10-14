from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from dotenv import load_dotenv

import os


load_dotenv()


# -----------------------------
# ENV VARIABLES
# -----------------------------

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")


# -----------------------------
# FASTAPI
# -----------------------------

app = FastAPI()


# -----------------------------
# AZURE OPENAI CLIENT
# -----------------------------

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)

deployment = AZURE_OPENAI_DEPLOYMENT


# -----------------------------
# AZURE AI SEARCH CLIENT
# -----------------------------

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <html>
    <body style="font-family: Arial; padding: 20px;">

    <h2>Enterprise RAG Assistant</h2>

    <form action="/chat" method="post">

    <textarea name="message" rows="6" cols="60"></textarea>

    <br><br>

    <button type="submit">Ask</button>

    </form>

    </body>
    </html>
    """


# -----------------------------
# CHAT ROUTE
# -----------------------------

@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):

    results = search_client.search(message)

    context = ""

    for result in results:
        context += str(result) + "\n"


    prompt = f"""
    Use ONLY the following enterprise knowledge:

    {context}

    Answer this question:

    {message}
    """


    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    answer = completion.choices[0].message.content


    return f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">

    <h2>Grounded AI Response</h2>

    <div style="white-space: pre-wrap; line-height: 1.6;">
    {answer}
    </div>

    <br><br>

    <a href="/">Go Back</a>

    </body>
    </html>
    """