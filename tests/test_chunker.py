from rag_brain.ingestion.chunker import split_text


SAMPLE_TEXT = """
Artificial intelligence is transforming industries worldwide.
Machine learning models learn patterns from data.
Deep learning uses neural networks with many layers.
Natural language processing enables computers to understand text.
Computer vision allows machines to interpret images.
Reinforcement learning trains agents through rewards and penalties.
""" * 20


# ── TESTS ─────────────────────────────────────────────

def test_split_returns_list():
    chunks = split_text(SAMPLE_TEXT)

    assert isinstance(chunks, list)


def test_split_produces_multiple_chunks():
    chunks = split_text(SAMPLE_TEXT)

    assert len(chunks) > 1


def test_chunks_have_content():
    chunks = split_text(SAMPLE_TEXT)

    for chunk in chunks:
        assert len(chunk.page_content) > 0


def test_chunk_size_respected():
    chunks = split_text(SAMPLE_TEXT)

    for chunk in chunks:
        assert len(chunk.page_content) <= 600


def test_empty_text_returns_empty():
    chunks = split_text("")

    assert chunks == []