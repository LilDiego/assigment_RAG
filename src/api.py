import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

# Ensure 'src' is in the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modules
from search_answers import load_faiss_index, search_answer  
from read_pdf import read_pdf
from chunking import chunk_text

# Initialize FastAPI
app = FastAPI()

# Corrected PDF path (inside 'documents/' folder)
PDF_PATH = os.path.join(os.path.dirname(__file__), "../documents/1210-Insurance-2030-The-impact-of-AI-on-the-future-of-insurance-_-McKinsey-Company.pdf")

# Ensure the PDF file exists before loading it
if not os.path.exists(PDF_PATH):
    print(f"❌ Error: The file '{PDF_PATH}' was not found.")
    sys.exit(1)

# Load FAISS index and handle errors
try:
    index, page_map = load_faiss_index()
except FileNotFoundError as e:
    print(f"❌ Error loading FAISS index: {e}")
    index, page_map = None, None  # Prevent crash

# Load the document text and split it into fragments
document_text = read_pdf(PDF_PATH)
text_chunks = chunk_text(document_text)

# Define a request model for the API
class QueryRequest(BaseModel):
    query: str

@app.post("/search")
def get_response(request: QueryRequest):
    """API endpoint to retrieve answers based on the document."""
    
    if index is None:
        return {"error": "FAISS index not loaded. Please check the vectorstore."}

    results = search_answer(request.query, index, text_chunks, page_map)  
    return {"responses": [{"text": r[0], "page": r[1]} for r in results]}

# Automatically start the API if the script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
