# Architecture

Pipeline:
1) PDF -> text extraction (PyPDF)
2) Chunking -> overlapping chunks (RecursiveCharacterTextSplitter)
3) Embedding -> FastEmbed (bge-small-en-v1.5)
4) Storage -> ChromaDB persistent collection
5) Retrieval -> vector search (top_k)
6) Safety gate -> MAX_DISTANCE
7) Fallback -> lexical keyword search (hybrid)
8) Generation -> Groq LLM (qwen/qwen3.8-27b) with evidence + citations