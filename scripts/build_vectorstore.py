from pathlib import Path
import re

import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastembed import TextEmbedding

PDF_PATH = Path("data/sample.pdf")
DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_chunks"

def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Missing PDF: {PDF_PATH.resolve()}")

    client = chromadb.PersistentClient(path=DB_DIR)

    # reset collection each run while developing
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    reader = PdfReader(str(PDF_PATH))

    documents, metadatas, ids = [], [], []
    for page_num, page in enumerate(reader.pages, start=1):
        page_text = clean_text(page.extract_text() or "")
        if not page_text:
            continue

        chunks = splitter.split_text(page_text)
        for chunk_in_page, chunk in enumerate(chunks):
            ids.append(f"p{page_num}_c{chunk_in_page}")
            documents.append(chunk)
            metadatas.append({"page": page_num, "chunk_in_page": chunk_in_page})

    embeddings = [e.tolist() for e in embedder.embed(documents)]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("PDF indexed:", PDF_PATH)
    print("Total pages:", len(reader.pages))
    print("Total stored chunks:", collection.count())
    print("DB directory:", Path(DB_DIR).resolve())

if __name__ == "__main__":
    main()