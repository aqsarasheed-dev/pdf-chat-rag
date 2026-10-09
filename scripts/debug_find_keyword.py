import chromadb

DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_chunks"

KEYWORDS = ["guardrail", "guardrails", "security"]

def main():
    client = chromadb.PersistentClient(path=DB_DIR)
    col = client.get_collection(COLLECTION_NAME)

    data = col.get(include=["documents", "metadatas"])
    docs = data["documents"]
    metas = data["metadatas"]

    hits = 0
    for doc, meta in zip(docs, metas):
        low = doc.lower()
        if any(k in low for k in KEYWORDS):
            hits += 1
            print("HIT:", meta)
            print(doc[:400])
            print("-" * 60)

    print("Total chunks:", len(docs))
    print("Keyword hits:", hits)

if __name__ == "__main__":
    main()