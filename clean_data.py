import re

def clean_text(text):
    """Cleans extracted text by removing unwanted metadata, headers, URLs, page numbers, punctuation, and extra spaces."""
    # convert to lower case
    text = text.lower()

    # Remove dates (e.g., 5/28/2018, May 2018)
    text = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}|\b\w+\s\d{4}\b", "", text)

    # Remove repeated headers and titles
    text = re.sub(r"Insurance 2030.*?McKinsey & Company", "", text, flags=re.IGNORECASE)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove pagination artifacts (e.g., "1/13", "2/13")
    text = re.sub(r"\b\d{1,2}/\d{1,2}\b", "", text)

    # Remove cookie disclaimers or irrelevant text
    text = re.sub(r"McKinsey uses cookies.*?By using this Site or clicking on OK", "", text, flags=re.DOTALL)

    # Remove exhibit numbers and section markers (e.g., "Exhibit 1", "Exhibit 2")
    text = re.sub(r"Exhibit\s\d+", "", text)

    # Remove all punctuation (except letters and numbers)
    text = re.sub(r"[^\w\s]", "", text)  # Removes .,;:/?!(){}[]-_ etc.

    # Remove extra spaces and line breaks
    text = re.sub(r"\s+", " ", text).strip()

    return text
