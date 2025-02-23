
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="future_ai")


user_query = input("What do you want to know about The impact of AI on the future of insurance?\n\n")

results = collection.query(
    query_texts=[user_query], #We can ask multiple queries, but here is only one
    n_results=5 #this ensure to get the most revelant result
)

# Concatenamos los resultados recuperados
context = "\n\n".join([" ".join(doc) for doc in results['documents']])

#print(results['documents'])
#print(results['metadatas'])

client = OpenAI()

system_prompt = """
You are a helpful assistant answering questions about the impact of AI on the future of insurance.
Please use the following documents to help you answer the user's question. If multiple documents are retrieved, synthesize the information and provide a complete answer.

The following documents are relevant:
--------------------
The data:

"""+str(results['documents'])+"""
"""

#print(system_prompt)

response = client.chat.completions.create(
    model="gpt-4o",
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}    
    ],
    temperature=0.3
)

print("\n\n---------------------\n\n")

print(response.choices[0].message.content)