import fitz

def extract_text_from_pdf(pdf_bytes: bytes) -> tuple[str, int]:
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        num_pages = len(doc)
        for page in doc:
            text += page.get_text()
    return text.strip(), num_pages