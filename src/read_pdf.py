import os
import pypdf

# PDF file name
PDF_FILENAME = "1210-Insurance-2030-The-impact-of-AI-on-the-future-of-insurance-_-McKinsey-Company.pdf"

# Path to the PDF inside the 'test/documents' folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Gets the path of 'test'
DOCUMENTS_PATH = os.path.join(BASE_DIR, "documents", PDF_FILENAME)  # Correct path to the PDF
DOCUMENTS_PATH = os.path.abspath(DOCUMENTS_PATH)  # Converts the path to an absolute one

def read_pdf(pdf_path):
    """Reads a PDF file and returns a list of tuples (text, page number)."""
    pages_text = []
    try:
        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(reader.pages, start=1):  # Start at page 1
                text = page.extract_text()
                if text:  # Avoid adding empty pages
                    pages_text.append((text, page_num))
    except FileNotFoundError:
        print(f"❌ Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"❌ Error reading the PDF: {e}")
    return pages_text

if __name__ == "__main__":
    pdf_pages = read_pdf(DOCUMENTS_PATH)  # Use the correct file name

    # Check if text was extracted successfully
    if pdf_pages:
        print(f"✅ Successfully extracted text from {len(pdf_pages)} pages.")
        print("\n🔹 First 500 characters from the first page:\n")
        print(pdf_pages[0][0][:500])  # Show only the first 500 characters of the first page
        print(f"\n📄 This content is from page {pdf_pages[0][1]}")
    else:
        print("⚠️ No text could be extracted from the PDF. Check the file or try another library.")
