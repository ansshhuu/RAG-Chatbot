from rag_brain.config import TOP_K

def get_retriever(vectordb):
    return vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k":TOP_K}
    )

