from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import openai
from clean_data import clean_text
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="future_ai")

# loading the document

loader = PyPDFDirectoryLoader(DATA_PATH)

raw_documents = loader.load()

#clean data

preprocessed_documents = []
for doc in raw_documents:
    cleaned_text = clean_text(doc.page_content)  # Clean only the text, not the whole object
    doc.page_content = cleaned_text  # Store cleaned text back in the object
    preprocessed_documents.append(doc)  # Add to the list

# #Print information about the document CHECK CLEANING DATA
# print(f"Number of documents loaded: {len(raw_documents)}")
# for doc in raw_documents:
#     # print(f"Document Metadata: {doc.metadata}")
#     print(f"Document Content: {doc.page_content[:500]}...")

# # Guardar el contenido en un archivo txt
# with open("preprocessed_documents.txt", "w", encoding="utf-8") as file:
#     for doc in preprocessed_documents:
#         #  file.write(f"Document Metadata: {doc.metadata}\n")  # Si tienes metadata que quieras incluir
#         file.write(f"Document Content: {doc.page_content}\n\n")  # Escribe el contenido completo de cada documento


# splitting the document

size = 400

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=size,
    chunk_overlap=(size*0.15),
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(preprocessed_documents)

# # VERIFY CONTENT CHUNKS
# print(f"Total number of chunks created: {len(chunks)}")
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i+1}:")
#     print(f"Content: {chunk.page_content[:500]}...")  # Mostramos los primeros 500 caracteres
#     # print(f"Metadata: {chunk.metadata}")
#     print("-" * 80)

# preparing to be added in chromadb

documents = []
metadata = []
ids = [] #Keep track of every single chunk that we put on the database, if we need to delete or change any chunk

##ESTA SERA MI MODIFICACION CON GENERANDO LOS CHUNKS COM EL MODELO DE EMBEDDINGS.

# Generar embeddings con OpenAI
embeddings = []

i = 0
for chunk in chunks:
    # Generar embedding para cada fragmento con OpenAI
    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Puedes elegir otro modelo si lo prefieres
        input=chunk.page_content
    )
    chunk_embedding = response.data[0].embedding # Extraemos el embedding del resultado
    embeddings.append(chunk_embedding)
    
    documents.append(chunk.page_content)
    ids.append("ID" + str(i))
    metadata.append(chunk.metadata)
    
    i += 1

# adding to chromadb


collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)