import os
import faiss
import numpy as np
import pickle  # To save the chunk-page mapping
from sentence_transformers import SentenceTransformer
from chunking import chunk_text
from read_pdf import read_pdf

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Project root folder
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore")
os.makedirs(VECTORSTORE_PATH, exist_ok=True)  # Ensure the folder exists

# Paths for FAISS index and page mapping file
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_PATH, "index_faiss_hf")
PAGE_MAP_PATH = os.path.join(VECTORSTORE_PATH, "page_map.pkl")

# PDF path
PDF_FILENAME = "1210-Insurance-2030-The-impact-of-AI-on-the-future-of-insurance-_-McKinsey-Company.pdf"
PDF_PATH = os.path.join(BASE_DIR, "documents", PDF_FILENAME)

# Load Hugging Face model for generating embeddings
print("🔄 Loading embedding model...")
hf_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded successfully.")

def create_embeddings_hf(chunks_pages):
    """Generates embeddings and saves the FAISS index along with page numbers."""
    
    # Separate text chunks and their page numbers
    texts = [chunk for chunk, _ in chunks_pages]
    pages = [page for _, page in chunks_pages]

    if not texts:
        print("⚠️ No text available to generate embeddings.")
        return

    print(f"🔄 Generating embeddings for {len(texts)} chunks...")
    embeddings = hf_model.encode(texts)  # Convert text to vectors
    embeddings = np.array(embeddings, dtype="float32")  # Convert to FAISS format

    # Create a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the FAISS index
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save the chunk → page mapping
    with open(PAGE_MAP_PATH, "wb") as f:
        pickle.dump(pages, f)

    print(f"✅ {len(chunks_pages)} embeddings generated and saved in {FAISS_INDEX_PATH}")
    print(f"✅ Page mapping saved in {PAGE_MAP_PATH}")

if __name__ == "__main__":
    print(f"🔄 Reading PDF from: {PDF_PATH}")
    pdf_text = read_pdf(PDF_PATH)

    if pdf_text:
        chunks_pages = chunk_text(pdf_text)  # Now returns [(chunk, page)]
        create_embeddings_hf(chunks_pages)
    else:
        print("⚠️ Could not extract text from the PDF. Check the path or try another library.")
