from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_brain.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.create_documents([text])