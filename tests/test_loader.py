import pytest
from pypdf import PdfWriter

from rag_brain.ingestion.loader import load_pdf


# ── FIXTURES ─────────────────────────────────────────

@pytest.fixture
def sample_pdf(tmp_path):
    """Create a minimal PDF for testing."""

    pdf_path = tmp_path / "test.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    with open(pdf_path, "wb") as f:
        writer.write(f)

    return str(pdf_path)


# ── TESTS ─────────────────────────────────────────────

def test_load_pdf_returns_string(sample_pdf):
    result = load_pdf(sample_pdf)

    assert isinstance(result, str)


def test_load_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_pdf("nonexistent.pdf")


def test_load_pdf_empty_pages(sample_pdf):
    result = load_pdf(sample_pdf)

    assert result == ""