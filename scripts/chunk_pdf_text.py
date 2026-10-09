from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = Path("data/sample.pdf")

def extract_all_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    texts = []
    for i, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        # Keep page markers (we'll use later for citations)
        texts.append(f"\n\n[PAGE {i}]\n{page_text}")
    return "\n".join(texts)

def basic_clean(text: str) -> str:
    # Remove excessive whitespace (PDFs often insert lots of line breaks/spaces)
    text = text.replace("\u00a0", " ")  # non-breaking spaces
    # collapse repeated spaces
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)

def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Missing: {PDF_PATH.resolve()}")

    raw = extract_all_text(PDF_PATH)
    cleaned = basic_clean(raw)
    chunks = chunk_text(cleaned)

    print("Total characters (raw):", len(raw))
    print("Total characters (cleaned):", len(cleaned))
    print("Total chunks:", len(chunks))
    print("-" * 60)

    # Show first 2 chunks
    for idx in range(min(2, len(chunks))):
        c = chunks[idx]
        print(f"[CHUNK {idx}] chars:", len(c))
        print(c[:500])
        print("-" * 60)

if __name__ == "__main__":
    main()