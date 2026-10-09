from pathlib import Path
from pypdf import PdfReader

PDF_PATH = Path("data/sample.pdf")

def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at: {PDF_PATH.resolve()}")

    reader = PdfReader(str(PDF_PATH))
    print("PDF loaded:", PDF_PATH)
    print("Total pages:", len(reader.pages))
    print("-" * 60)

    # Extract text from first 2 pages for testing
    for i in range(min(2, len(reader.pages))):
        page = reader.pages[i]
        text = page.extract_text() or ""
        print(f"[Page {i+1}] extracted chars:", len(text))
        print(text[:500])  # preview first 500 chars
        print("-" * 60)

if __name__ == "__main__":
    main()