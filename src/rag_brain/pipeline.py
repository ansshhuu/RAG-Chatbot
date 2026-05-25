from rag_brain.ingestion.loader import load_pdf
from rag_brain.ingestion.chunker import split_text
from rag_brain.ingestion.embedder import get_embedder
from rag_brain.retrieval.vector_store import store_embeddings, load_vectorstore
from rag_brain.retrieval.retriever import get_retriever
from rag_brain.generation.generator import build_qa_chain

def ingest_pdf(file_path: str):
    print("Loading PDF...")
    text = load_pdf(file_path)

    print("Splitting text into chunks...")
    chunks = split_text(text)

    if not chunks:
        print("No chunks. Empty PDF?")
        return 0

    print("Creating embeddings...")
    embedder = get_embedder()

    print("Storing embeddings in ChromaDB...")
    store_embeddings(chunks, embedder)

    print(f"Done. {len(chunks)} chunks stored.")
    return len(chunks)


def ask_question(question: str) -> dict:
    embedder = get_embedder()
    vectordb = load_vectorstore(embedder)
    retriever = get_retriever(vectordb)
    chain = build_qa_chain(retriever)

    docs = retriever.invoke(question)
    raw = chain.invoke(question)

    if isinstance(raw, dict):
        answer = raw.get("result", "")
    else:
        answer = raw

    return {
        "answer": answer,
        "sources": [doc.page_content[:200] for doc in docs]
    }