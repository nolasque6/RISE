import io
from pypdf import PdfReader

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file = io.BytesIO(pdf_bytes)
    reader = PdfReader(pdf_file)
    extracted_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
            
    return extracted_text.strip()