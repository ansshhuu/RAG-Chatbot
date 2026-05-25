from unittest.mock import MagicMock, patch

from pypdf import PdfWriter
from rag_brain.pipeline import ingest_pdf, ask_question


def test_ingest_pdf_returns_chunk_count(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with open(pdf_path, "wb") as f:
        writer.write(f)

    with patch("rag_brain.pipeline.get_embedder"), \
         patch("rag_brain.pipeline.store_embeddings"):

        result = ingest_pdf(str(pdf_path))

    assert isinstance(result, int)


def test_ask_question_returns_dict():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {
        "result": "This is a test answer.",
        "source_documents": [
            MagicMock(page_content="chunk content here")
        ]
    }

    with patch("rag_brain.pipeline.get_embedder"), \
         patch("rag_brain.pipeline.load_vectorstore"), \
         patch("rag_brain.pipeline.get_retriever"), \
         patch("rag_brain.pipeline.build_qa_chain", return_value=mock_chain):

        result = ask_question("What is AI?")

    assert "answer" in result
    assert "sources" in result
    assert isinstance(result["answer"], str)
    assert isinstance(result["sources"], list)


def test_ask_question_answer_is_string():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {
        "result": "Test answer",
        "source_documents": []
    }

    with patch("rag_brain.pipeline.get_embedder"), \
         patch("rag_brain.pipeline.load_vectorstore"), \
         patch("rag_brain.pipeline.get_retriever"), \
         patch("rag_brain.pipeline.build_qa_chain", return_value=mock_chain):

        result = ask_question("test?")

    assert isinstance(result["answer"], str)