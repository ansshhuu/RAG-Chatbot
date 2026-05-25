import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL=os.getenv("LLM_MODEL","llama3-8b-8192")
CHROMA_PERSIST_DIR=os.getenv("CHROMA_PERSIST_DIR","./vectorstore")
CHUNK_SIZE=int(os.getenv("CHUNK_SIZE",500))
CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP",50))
TOP_K=int(os.getenv("TOP_K",4))