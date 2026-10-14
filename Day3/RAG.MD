
# RAG Agent on Azure AI Foundry
Before you start

-A storage account (aimldataset) and an Azure AI Search service in the same subscription.
-An embedding model deployed in Foundry, for example text-embedding-3-small (Models → Deploy). The import wizard needs it.
#Part 1: Upload the files to storage
-Azure portal → Storage accounts → aimldataset.
-Data storage → Containers → + Container.
-Name: helpdesk-kb (lowercase, no spaces)
-Access level: Private
-Click Create.
-Open helpdesk-kb → Upload, select all your .txt files, then Upload.

#✅ Check: all the files are listed in the container.

#Part 2: Import the data into Azure AI Search
-Azure portal → your Azure AI Search service → Overview → Import data (or Import data (new)).
-Data source: choose Azure Data Lake Storage Gen2.
-This only works if the storage account has hierarchical namespace enabled. If aimldataset isn’t listed or shows an error, go back and choose Azure Blob Storage; the rest of the steps are the same.
-Scenario: choose RAG.
#Section 1: Connect to your data
Field	Value
Subscription	Your subscription
Storage account	aimldataset
Container	helpdesk-kb (the one you created)
Other fields	Leave the defaults

Click Next.

Section 2: Vectorize your text
Field	Value
Kind	Microsoft Foundry (may be labelled Azure AI Foundry / Azure OpenAI)
Project / resource	Your Foundry project
Model deployment	Your embedding model, for example text-embedding-3-small
Authentication type	API key
Checkbox	Tick the acknowledgement (it confirms embedding calls are billed)

Click Next.

Remaining screens
Keep all defaults (image vectorization off, semantic ranker on, schedule Once). Click Next on each.
Review and create: set Objects name prefix to your index name, for example helpdesk-kb-index.
Click Create. Indexing takes about 1–3 minutes for a few text files.

✅ Check: Search service → Indexes shows helpdesk-kb-index with a document count above 0.

A minimal, editable ReAct-style agent built with LangGraph, using an Azure AI
Foundry model deployment (via Azure OpenAI) as the LLM.

## 1. Get your Azure AI Foundry values

In the [Azure AI Foundry portal](https://ai.azure.com):

1. Open your project → **Deployments** → note the **deployment name** of the
   chat model you deployed (e.g. `gpt-4o`).
2. Go to your project's **Overview** or the underlying Azure OpenAI resource
   → **Keys and Endpoint** → copy the **endpoint** and **key**.

## 2. Set up the project in VS Code

```bash
# from the folder containing agent.py
python -m venv .venv

# activate it
.venv\Scripts\activate           # Windows (PowerShell: .venv\Scripts\Activate.ps1)

pip install -r requirements.txt
```

In VS Code:
- Install the **Python** extension (ms-python.python) if you don't have it.
- `Ctrl/Cmd+Shift+P` → "Python: Select Interpreter" → choose the `.venv` you
  just created.

## 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your real values:

```
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
AZURE_SEARCH_ENDPOINT=https://<resource>.search.windows.net
AZURE_SEARCH_KEY=<your-api-key>
AZURE_SEARCH_INDEX=<your-index>
```

`.env` is loaded automatically by `python-dotenv` in `agent.py` — don't commit
it to source control.

## 4. Run it

```bash
python agent.py
```

Try prompts like:
- "What's the weather in Seattle?"
- "What's 23 * 17 + 4?"
- "What's the weather in Austin, and also what's 100 / 4?"

You'll see the agent call the `get_weather` or `calculator` tools
automatically when needed, then respond with a final answer.

## How it's structured

- **Tools** (`get_weather`, `calculator`) — plain Python functions decorated
  with `@tool`. Replace these with your real integrations (internal APIs,
  databases, search, Azure AI Search, etc.).
- **`AzureChatOpenAI`** — the LangChain wrapper that talks to your Azure AI
  Foundry deployment.
- **`StateGraph`** — defines the agent's control flow explicitly:
  - `agent` node: calls the LLM, which decides to answer directly or call a
    tool.
  - `tools` node (`ToolNode`): executes whichever tool(s) the LLM requested.
  - `tools_condition`: routes to `tools` if the LLM asked for a tool call,
    otherwise routes to `END`.
  - The graph loops `agent -> tools -> agent` until the LLM gives a final
    answer with no more tool calls.

## Extending this

- **Add more tools**: write a new `@tool`-decorated function and add it to
  the `tools` list.
- **Add memory/persistence across sessions**: swap `graph_builder.compile()`
  for `graph_builder.compile(checkpointer=...)` using LangGraph's
  `MemorySaver` or a SQLite/Postgres checkpointer.
- **Multi-agent / supervisor pattern**: if you need multiple specialized
  agents coordinated by a router, that's a different graph shape (a
  supervisor node routing to sub-agent nodes) — let me know if you want that
  version instead of the single ReAct agent above.
- **Streaming**: use `graph.stream(...)` instead of `graph.invoke(...)` to
  stream tokens/steps back to a UI.
- **VS Code debugging**: add a `launch.json` with a `"program": "agent.py"`
  Python configuration to set breakpoints inside tool functions or the graph
  nodes.
