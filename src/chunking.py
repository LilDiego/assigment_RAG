import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from read_pdf import read_pdf

# Define the PDF file name
PDF_FILENAME = "1210-Insurance-2030-The-impact-of-AI-on-the-future-of-insurance-_-McKinsey-Company.pdf"

# Get the project's base directory ('test' folder)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Construct the correct path to the PDF in the 'documents' folder
PDF_PATH = os.path.join(BASE_DIR, "documents", PDF_FILENAME)
PDF_PATH = os.path.abspath(PDF_PATH)  # Ensure the path is absolute

def chunk_text(pages_text, chunk_size=500, chunk_overlap=50):
    """Splits text into chunks while keeping the page number."""
    chunks_with_pages = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  
        chunk_overlap=chunk_overlap,  
        length_function=len  
    )

    for text, page in pages_text:  # Iterate over each page
        chunks = splitter.split_text(text)  # Split the page's text
        for chunk in chunks:
            chunks_with_pages.append((chunk, page))  # Store the chunk with its page number

    return chunks_with_pages

if __name__ == "__main__":
    # Read the PDF
    pages_text = read_pdf(PDF_PATH)  # Now returns [(text, page), ...]

    if pages_text:
        # Split into chunks
        chunks = chunk_text(pages_text)

        # Display the first 3 chunks
        print(f"✅ Text split into {len(chunks)} chunks. First 3 chunks:\n")
        for i, (chunk, page) in enumerate(chunks[:3]):
            print(f"🔹 Chunk {i+1} (Page {page}):\n{chunk}\n{'-'*80}")
    else:
        print("⚠️ No text could be extracted from the PDF. Check the file or try another library.")
