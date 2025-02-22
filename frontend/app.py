import streamlit as st
import requests

# Configure Streamlit Page
st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("📘 Virtual AI Assistant - RAG Document Search")

# User input field
query = st.text_input("🔎 Enter your question about the document:")

if query:
    # Call the FastAPI backend
    url = "http://localhost:8000/search"  # Make sure FastAPI is running on this port
    response = requests.post(url, json={"query": query})

    if response.status_code == 200:
        results = response.json()["responses"]
        st.write("✅ **Found answers:**")
        for i, r in enumerate(results):
            st.write(f"**{i+1}. Page {r['page']}**")
            st.info(r["text"])
    else:
        st.error("❌ Error retrieving response from API.")
