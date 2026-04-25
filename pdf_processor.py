import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """Read all text from a PDF file"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # overlap so context isn't lost at edges

    return chunks


def process_pdf(pdf_path: str) -> list[str]:
    """Full pipeline — extract text then chunk it"""
    print(f"Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    print(f"Total characters extracted: {len(text)}")

    chunks = chunk_text(text)
    print(f"Total chunks created: {len(chunks)}")

    return chunks