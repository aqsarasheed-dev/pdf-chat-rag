import chromadb
from fastembed import TextEmbedding

DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_chunks"

def main():
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    query = "What is LLM observability?"
    query_emb = next(embedder.embed([query])).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    print("Query:", query)
    print("-" * 60)

    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        meta = results["metadatas"][0][i]
        dist = results["distances"][0][i]
        print(f"Result {i+1} | distance={dist:.4f} | page={meta.get('page')}")
        print(doc[:250])
        print("-" * 60)

if __name__ == "__main__":
    main()