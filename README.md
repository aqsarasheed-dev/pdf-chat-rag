# PDF Chat (RAG) — Groq + Chroma + FastEmbed

Chat with a PDF using **Retrieval Augmented Generation (RAG)**:
PDF → extract text → chunk → embed → store in vector DB → retrieve relevant chunks → answer with citations.

This project is built step-by-step for learning and portfolio purposes.

---

## Features
- Extract text from PDF (PyPDF)
- Chunking with overlap (LangChain text splitters)
- Vector database: **ChromaDB** (persistent local storage)
- Free local embeddings: **FastEmbed** (`BAAI/bge-small-en-v1.5`)
- Free LLM API: **Groq** (tested with `qwen/qwen3.8-27b`)
- CLI chat interface
- Citations using PDF page metadata
- Hallucination reduction:
  - retrieval confidence gate (`MAX_DISTANCE`)
  - lexical fallback for short/keyword queries
  - prompt requires evidence/quotes

---

## Tech Stack
- Python
- Groq API (LLM)
- ChromaDB (vector store)
- FastEmbed (embeddings)
- PyPDF (PDF parsing)
- LangChain Text Splitters (chunking)

---

## Setup (Windows)
### 1) Create & activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```

### 2) Install dependencies

python -m pip install python-dotenv groq pypdf chromadb fastembed langchain-text-splitters
