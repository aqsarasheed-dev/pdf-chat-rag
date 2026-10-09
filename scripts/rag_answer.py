import os
from dotenv import load_dotenv

import chromadb
from fastembed import TextEmbedding
from groq import Groq

# ------------ Config ------------
DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_chunks"

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "qwen/qwen3.8-27b"

TOP_K = 8
MAX_DISTANCE = 0.45  #   smaller distance = more relevant (tune later)
SHOW_SOURCES = True  # set False if you want cleaner output
# --------------------------------


def build_prompt(question: str, docs: list[str], metas: list[dict]) -> tuple[str, str]:
    """Create (system_prompt, user_prompt) for RAG answering."""
    context_blocks = []
    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
        page = meta.get("page", "?")
        context_blocks.append(f"[Source {i} | page {page}]\n{doc}")

    context = "\n\n---\n\n".join(context_blocks)

    
    system_prompt = (
    "You are a PDF assistant.\n"
    "RULES:\n"
    "1) Answer ONLY using the provided sources.\n"
    "2) If the sources do NOT explicitly contain the answer, say exactly: "
    "\"I don't know based on the document.\"\n"
    "3) You MUST include 1-2 exact quotes from the sources as Evidence.\n"
    "4) Add citations like (page X).\n"
)
    

    user_prompt = f"""SOURCES:
{context}

QUESTION: {question}

Instructions:
- First, find the exact sentence(s) in the SOURCES that answer the question.
- If you cannot find exact supporting sentences, respond: "I don't know based on the document."
- Otherwise answer briefly and include:

Evidence:
- "..." (page X)
- "..." (page Y)
- "..." (page Z)"""
    return system_prompt, user_prompt

def find_keyword_in_db(collection, keyword: str, limit: int = 5):
    """Return up to `limit` chunks that contain the keyword (case-insensitive)."""
    data = collection.get(include=["documents", "metadatas"])
    keyword = keyword.lower().strip()

    hits = []
    for doc, meta in zip(data["documents"], data["metadatas"]):
        if keyword in doc.lower():
            hits.append((meta, doc))
            if len(hits) >= limit:
                break
    return hits


def lexical_fallback(collection, query: str, top_k: int = 3):
    """
    Fallback when vector retrieval is weak.
    Simple keyword search over stored chunks.
    """
    data = collection.get(include=["documents", "metadatas"])
    docs = data["documents"]
    metas = data["metadatas"]

    tokens = [t.strip(".,!?()[]{}:;\"'").lower() for t in query.split()]
    tokens = [t for t in tokens if len(t) >= 5]  # ignore short words like "llm"
    if not tokens:
        return [], []

    key = max(tokens, key=len)  # choose the longest word from the query

    scored = []
    for doc, meta in zip(docs, metas):
        pos = doc.lower().find(key)
        if pos != -1:
            scored.append((pos, doc, meta))

    scored.sort(key=lambda x: x[0])
    scored = scored[:top_k]

    return [x[1] for x in scored], [x[2] for x in scored]
def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    # 1) Initialize clients ONCE (important for performance)
    groq_client = Groq(api_key=api_key)

    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    try:
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
    except Exception:
        raise RuntimeError(
            f"Chroma collection '{COLLECTION_NAME}' not found. "
            f"Run scripts/build_vectorstore.py first."
        )

    embedder = TextEmbedding(model_name=EMBED_MODEL)

    print("Chat with your PDF.")
    print("Type your question. Type 'exit' to quit.")

    def retrieve(q: str):
        q_emb = list(embedder.embed([q]))[0].tolist()
        return collection.query(
            query_embeddings=[q_emb],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"],
        )

    # 2) Chat loop
    while True:
        question = input("\nYou: ").strip()

        # Command: /find <word> -> checks if the word exists in your indexed chunks
        if question.lower().startswith("/find "):
            kw = question[6:].strip()
            hits = find_keyword_in_db(collection, kw, limit=5)
            if not hits:
                print(f"Assistant: No chunks contain '{kw}'. (So the indexed PDF text doesn't include it.)")
            else:
                print(f"Assistant: Found {len(hits)} chunk(s) containing '{kw}':")
                for meta, doc in hits:
                    print(f"  page={meta.get('page')} chunk_in_page={meta.get('chunk_in_page')}")
                    print("  ", doc[:250])
                    print("-" * 50)
            continue

        if not question:
            continue

        if question.lower() == "exit":
            print("Bye.")
            break

        results = retrieve(question)
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        if not docs:
            print("Assistant: I don't know based on the document. (no retrieval results)")
            continue

        best_distance = dists[0]

        # --- pass 2: if weak match, expand the query and try again
        if best_distance > MAX_DISTANCE:
            expanded = (
                f"{question}. Focus on LLM safety, guardrails, security, "
                "prompt injection, policy, and risk."
            )
            results2 = retrieve(expanded)

            docs2 = results2["documents"][0]
            metas2 = results2["metadatas"][0]
            dists2 = results2["distances"][0]

            if docs2 and dists2 and dists2[0] < best_distance:
                docs, metas, dists = docs2, metas2, dists2
                best_distance = dists2[0]

        # final gate
                # final gate (with lexical fallback)
        if best_distance > MAX_DISTANCE:
            fb_docs, fb_metas = lexical_fallback(collection, question, top_k=3)
            if fb_docs:
                docs, metas = fb_docs, fb_metas
                dists = [best_distance] * len(docs)  # for debug printing only
            else:
                print("Assistant: I don't know based on the document. (retrieval confidence too low)")
                if SHOW_SOURCES:
                    print(f"Debug: best_distance={best_distance:.4f} (threshold={MAX_DISTANCE})")
                continue

        system_prompt, user_prompt = build_prompt(question, docs, metas)

        # Call Groq
        resp = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            max_tokens=300,
        )

        answer = resp.choices[0].message.content.strip()
        print("\nAssistant:", answer)

        # Deterministic citations from metadata 
        pages = sorted({m.get("page") for m in metas if m.get("page") is not None})
        if pages:
            print("Citations:", ", ".join([f"page {p}" for p in pages]))

        if SHOW_SOURCES:
            print("\nSources used:")
            for i, (meta, dist) in enumerate(zip(metas, dists), start=1):
                print(f"  Source {i}: page={meta.get('page')} distance={dist:.4f}")


if __name__ == "__main__":
    main()