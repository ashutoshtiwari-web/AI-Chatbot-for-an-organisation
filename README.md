# AI Chatbot for an Organisation 🤖

An **agentic HR assistant** built with LangGraph and LangChain that answers employee questions about **payroll**, **benefits**, and general HR policy — grounded in company documents via Retrieval-Augmented Generation (RAG), guarded by a safety classifier, and evaluated automatically with RAGAS + Langfuse.

---

## ✨ Overview

This project simulates a real-world internal HR chatbot for an organisation. Instead of a single LLM call, it uses a **multi-agent graph workflow** (via [LangGraph](https://github.com/langchain-ai/langgraph)) that:

1. Screens every query with a **guardrail agent** for unsafe or out-of-scope content.
2. Classifies **intent** (payroll, benefits, or general).
3. Routes the query to the right specialist agent, which fetches (mock) API data and/or retrieves relevant document chunks.
4. Generates a grounded answer using a local LLM (via [Ollama](https://ollama.com/)).
5. Scores the response for **relevancy** and **faithfulness** using RAGAS, and logs traces/scores to **Langfuse** for observability.

---

## 🏗️ Architecture

```
                ┌───────────────┐
   User Query → │  Guardrail    │ → unsafe? → End (blocked)
                │  Agent        │
                └──────┬────────┘
                       │ safe
                       ▼
                ┌───────────────┐
                │  Intent Agent │
                └──────┬────────┘
           ┌───────────┼───────────┐
           ▼           ▼           ▼
      ┌─────────┐ ┌──────────┐ ┌────────┐
      │ Payroll │ │ Benefits │ │  RAG   │
      │  Agent  │ │  Agent   │ │(Docs)  │
      └────┬────┘ └────┬─────┘ └───┬────┘
           └───────────┼───────────┘
                       ▼
                ┌───────────────┐
                │ Generate Node │ → Final Answer (streamed)
                │ (LLM + RAG)   │
                └──────┬────────┘
                       ▼
              RAGAS Evaluation + Langfuse Trace
```

The graph is defined in [`Graph.py`](./Graph.py) using `langgraph.graph.StateGraph`, with shared state modeled in [`User_query.py`](./User_query.py) (`GraphState`, a Pydantic model).

---

## 🧩 Key Components

| Component | File | Description |
|---|---|---|
| **Guardrail Agent** | `agents/GaurdrailAgent.py` | Classifies each query as `SAFE`, `OUT_OF_SCOPE`, `VIOLENCE`, `SELF_HARM`, `ILLEGAL`, `HATE`, or `PROMPT_INJECTION` before it reaches any other agent. |
| **Intent Agent** | `agents/intent_agent.py` | Classifies the query intent (`payroll`, `benefits`, `general`) using a prompt from `Prompts/intent_prompt.txt`. |
| **Payroll Agent** | `agents/payroll_agent.py` | Returns payroll/paycheck data (mocked; designed to be swapped for a real HRMS API call). |
| **Benefits Agent** | `agents/benefits_agent.py` | Returns benefits enrollment data (mocked; same production-ready pattern). |
| **RAG Pipeline** | `RAG.py` | Loads the HR policy PDF, chunks it, embeds it with `nomic-embed-text`, and stores/retrieves it from a persistent **ChromaDB** vector store. |
| **Response Generation** | `Graph.py` (`generate_node`) | Combines retrieved context + API data into a prompt and streams a response from a local Llama 3 model via Ollama. |
| **Evaluation** | `Evaluation/` | Builds a RAGAS-compatible dataset per turn and scores **Answer Relevancy** and **Faithfulness**. |
| **Observability** | `langfuse_client.py`, `Langfuse.env` | Sends traces and evaluation scores to [Langfuse](https://langfuse.com/) for monitoring. |
| **Security (WIP)** | `security/LLMGuard.py` | Additional input/output scanning (prompt injection detection, PII anonymization, sensitive-topic banning) via `llm-guard`. |

---

## 📂 Project Structure

```
.
├── Main.py                     # Entry point — interactive CLI chat loop
├── Graph.py                    # LangGraph workflow definition (nodes & routing)
├── User_query.py               # Shared GraphState (Pydantic model)
├── RAG.py                      # Document loading, chunking, embedding & retrieval
├── config.py                   # Environment variable loading
├── langfuse_client.py          # Langfuse client setup
│
├── agents/
│   ├── GaurdrailAgent.py       # Safety classifier
│   ├── intent_agent.py         # Intent classifier
│   ├── payroll_agent.py        # Payroll data agent
│   └── benefits_agent.py       # Benefits data agent
│
├── Prompts/
│   ├── intent_prompt.txt
│   ├── payroll_system_prompt.txt
│   └── benefits_system_prompt.txt
│
├── docs/
│   ├── HR_document File.pdf    # Source HR policy document (used for RAG)
│   ├── payroll_policy.txt
│   └── benefits_policy.txt
│
├── Evaluation/
│   ├── backend.py              # Async wrapper around RAGAS evaluation
│   ├── Dataset_bulider_for_raga.py
│   └── Ragas_worker.py         # RAGAS metrics: answer_relevancy, faithfulness
│
├── security/
│   └── LLMGuard.py             # Prompt injection / PII / sensitive-topic scanning
│
├── chroma_db/                  # Persisted vector store (auto-generated)
└── requirement.txt             # Python dependencies
```

---

## ⚙️ Tech Stack

- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://www.langchain.com/)
- **LLM & Embeddings:** [Ollama](https://ollama.com/) (`llama3`, `nomic-embed-text`) — runs fully locally
- **Vector Store:** [ChromaDB](https://www.trychroma.com/)
- **Evaluation:** [RAGAS](https://github.com/explodinggradients/ragas) (answer relevancy, faithfulness)
- **Observability:** [Langfuse](https://langfuse.com/)
- **Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Security:** [LLM Guard](https://github.com/protectai/llm-guard) (input/output scanning)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally, with the required models pulled:
  ```bash
  ollama pull llama3
  ollama pull nomic-embed-text
  ```
- A [Langfuse](https://langfuse.com/) account (free tier works) for trace logging — optional but wired in by default.

### Installation

```bash
# Clone the repository
git clone https://github.com/ashutoshtiwari-web/AI-Chatbot-for-an-organisation.git
cd AI-Chatbot-for-an-organisation

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt
```

### Configuration

Create a `.env` file in the project root with your own credentials (do **not** commit real keys):

```env
LANGFUSE_SECRET_KEY=""
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_BASE_URL=""
LLM_Model="llama3"
```

> ⚠️ **Security note:** The repository currently contains a committed `.env` file with sample keys. Before pushing further changes, rotate any real credentials, remove the file from version control, and add `.env` to `.gitignore`.

### Running the Chatbot

```bash
python Main.py
```

You'll be dropped into an interactive CLI:

```
User : What is my current 401k contribution?
```

The chatbot will classify intent, route to the Benefits agent, retrieve relevant policy context, stream back an answer, and log relevancy/faithfulness scores to Langfuse.

---

## 🧪 Evaluation

Every response is automatically scored with **RAGAS**:

- **Answer Relevancy** — how relevant the answer is to the question asked.
- **Faithfulness** — how well the answer is grounded in the retrieved context (i.e., reduces hallucination).

Scores are pushed to Langfuse alongside the full conversation trace for later review.

---

## 🗺️ Roadmap / Known Limitations

- [ ] Replace mocked `PayrollAgent` / `BenefitsAgent` API calls with real HRMS integrations.
- [ ] Add `timeoff` and `employee_profile` intents to the routing graph (currently only defined in the intent prompt, not yet wired into `Graph.py`).
- [ ] Finish and wire up `security/LLMGuard.py` for production-grade prompt-injection and PII protection.
- [ ] Remove committed secrets (`.env`, `Langfuse.env`, `LangfuseAPI.txt`) from version control.
- [ ] Add unit/integration tests and CI.
- [ ] Add a web-based front end (currently CLI-only).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

No license file is currently included in this repository. Consider adding one (e.g., MIT) to clarify usage rights for others.
