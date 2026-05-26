from langchain_chroma import Chroma
from rag_brain.config import CHROMA_PERSIST_DIR

def store_embeddings(chunks, embedder):
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        persist_directory=CHROMA_PERSIST_DIR
    )
    return vectordb

def load_vectorstore(embedder):
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embedder
    )