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
# CORE AGENT FUNCTION
# -----------------------------
def ask_agent(message: str) -> str:
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
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

# -----------------------------
# SIMPLE CLI LOOP
# -----------------------------
if __name__ == "__main__":
    print("Enterprise RAG Assistant (type 'exit' to quit)")
    while True:
        message = input("\nYou: ")
        if message.lower() in ("exit", "quit"):
            break
        answer = ask_agent(message)
        print(f"\nAssistant: {answer}")