import os
import faiss
import numpy as np
import pickle  # To load the page mapping
from sentence_transformers import SentenceTransformer
from chunking import chunk_text
from read_pdf import read_pdf

# Paths to the saved files
FAISS_INDEX_PATH = "vectorstore/index_faiss_hf"
PAGE_MAP_PATH = "vectorstore/page_map.pkl"  # File containing the page number mapping

# Load the Hugging Face model to generate embeddings
hf_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index():
    """Loads the FAISS index and the page mapping stored on disk."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"⚠️ File {FAISS_INDEX_PATH} not found. Generate the embeddings first.")
    
    index = faiss.read_index(FAISS_INDEX_PATH)

    # Load the fragment → page mapping
    if not os.path.exists(PAGE_MAP_PATH):
        raise FileNotFoundError(f"⚠️ File {PAGE_MAP_PATH} not found. Make sure the embeddings have been generated correctly.")
    
    with open(PAGE_MAP_PATH, "rb") as f:
        page_map = pickle.load(f)

    return index, page_map

def search_answer(question, index, fragments, page_map, top_k=3):
    """Searches for the most relevant answer in FAISS for a given question and displays the page."""
    # Convert the question into an embedding
    question_embedding = hf_model.encode([question])
    question_embedding = np.array(question_embedding, dtype="float32")

    # Search for the most similar fragments in FAISS
    distances, indices = index.search(question_embedding, top_k)

    # Retrieve the most relevant fragments and their pages
    answers = []
    for i in indices[0]:
        if i < len(fragments):
            answers.append((fragments[i], page_map[i]))  # (Text, Page)

    return answers

if __name__ == "__main__":
    # Load the FAISS index and the page mapping
    try:
        index, page_map = load_faiss_index()
    except FileNotFoundError as e:
        print(e)
        exit()

    # Get the absolute path of the PDF
    pdf_path = os.path.join(os.path.dirname(__file__), "../documents/1210-Insurance-2030-The-impact-of-AI-on-the-future-of-insurance-_-McKinsey-Company.pdf")

    # Check if the file exists before reading it
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        exit()

    # Regenerate the text fragments from the PDF
    pdf_text = read_pdf(pdf_path)
    fragments = [fragment for fragment, _ in chunk_text(pdf_text)]

    # Perform a query
    user_question = input("🔎 Enter your question: ")
    answers = search_answer(user_question, index, fragments, page_map)

    print("\n✅ Answer(s) found:\n")
    for i, (answer, page) in enumerate(answers):
        print(f"🔹 {i+1}. (Page {page})\n{answer}\n{'-'*80}")
