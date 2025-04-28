# backend/data_ingestion.py

import os
import json
import fitz  # PyMuPDF
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ------------------------------
# Settings
RAW_DOCS_PATH = "data/raw_docs/"
PROCESSED_CHUNKS_PATH = "data/processed_chunks/"
CHUNK_SIZE = 1000  # characters
CHUNK_OVERLAP = 100  # characters
# ------------------------------

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text):
    """Split large text into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks

def save_chunks(chunks, output_path):
    """Save text chunks to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

def process_document(api_name, doc_type, pdf_filename):
    """
    Process one PDF:
    - api_name: 'stripe', 'adyen', etc.
    - doc_type: 'business' or 'technical'
    - pdf_filename: filename inside raw_docs/
    """
    print(f"Processing {api_name} - {doc_type}...")
    
    pdf_path = os.path.join(RAW_DOCS_PATH, pdf_filename)
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    
    output_file = os.path.join(PROCESSED_CHUNKS_PATH, api_name, f"{doc_type}_chunks.json")
    save_chunks(chunks, output_file)

def main():
    """Main driver function to process all PDFs."""
    docs_to_process = [
        # Format: (api_name, doc_type, pdf_filename)
        ("stripe", "business", "stripe_business_info.pdf"),
        ("stripe", "technical", "stripe_technical_docs.pdf"),
        ("adyen", "business", "adyen_business_info.pdf"),
        ("adyen", "technical", "adyen_technical_docs.pdf"),
    ]
    
    for api_name, doc_type, pdf_filename in tqdm(docs_to_process):
        process_document(api_name, doc_type, pdf_filename)

if __name__ == "__main__":
    main()
