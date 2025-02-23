# ASSIGMENT

Mi solucion consistio en crear un sistema guadado en la carpeta prueba conformado de la carpeta documents que contiene el archivo PDF a buscar respuestas, la carpeta source que contiene el archivo read_pdf.py el cual se usa para leer el pdf ya montado en documents, el archivo chuking.py que utiliza la division de información del documento mediante el metodo RecursiveCharacterTextSplitter DE LOongChain con los parametros  chunk_size=500, chunk_overlap=50, el archivo generate_embeddings para la creacion de los embeddings con un modelo pre-entrenado como lo es hf_model = SentenceTransformer("all-MiniLM-L6-v2"), posteriormente el archivo search_answers para realizar consultas sobre el documento, y el archivo api, pero realizar la conexion del modelo con la intefaz grafica. Fuera dentro de la carpeta raiz "PRUEBA" esta la carpeta frontend, y dentro esta el archivo app.py que contiene el codigo para la creacion del frontend con Streamlit, afuerta en la carpeta principal tambien esta la carpeta vectorstore que guarda los vectores generados por el embeddings y finalmente esta la carpeta del ambiente virtual creado para este proyecto.

# Prueba Técnica - AI y PDF

Este proyecto implementa un sistema basado en inteligencia artificial para procesar documentos PDF y realizar consultas sobre su contenido. La solución utiliza *Sentence Transformers*, FAISS, y un frontend en Streamlit para interactuar con el modelo.

## Estructura del Proyecto

📂 `prueba/`  
├── 📄 `README.md` - Descripción general del proyecto  
├── 📄 `requirements.txt` - Librerías necesarias  
├── 📂 `src/`  
│   ├── 📄 `read_pdf.py` - Extrae texto del PDF  
│   ├── 📄 `chunking.py` - Divide el texto en fragmentos  
│   ├── 📄 `generate_embeddings.py` - Genera embeddings e indexa con FAISS  
│   ├── 📄 `search_answers.py` - Busca respuestas en FAISS  
│   ├── 📄 `api.py` - API con FastAPI
│   ├── 📄 `openai_api.py` - API de OpenAI
│   ├── 📄 `logging_config` - Log funciones
├── 📂 `vectorstore/` - Almacena los embeddings y el índice FAISS  
├── 📂 `frontend/` - Carpeta para la interfaz  
│   └── 📄 `app.py` - Aplicación en Streamlit
├── 📄 `gitignore` - Archivos ignorados

# Pasos a seguir

## Crear ambiente virtual

python3 -m venv testenv

source testenv/bin/activate

testenv\Scripts\activate

## instalar dependencias

pip install -r requirements.txt

## ejecutar la API

python3 src/api.py

## ejecutar la integaz gafica.

python3 -m streamlit run frontend/app.py



