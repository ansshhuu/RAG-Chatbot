# RAG Chatbot

> Chat with your PDF documents using Retrieval-Augmented Generation (RAG), semantic search, ChromaDB, and Groq LLM.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-success)

---

## Features

- PDF document upload
- Automatic PDF text extraction
- Smart text chunking
- Embedding generation using Sentence Transformers
- Chroma vector database storage
- Semantic retrieval
- Groq-powered LLM responses
- Source chunk transparency
- Chat interface with memory
- Docker support
- GitHub CI pipeline
- Automated tests

---

## Demo Screenshots



## Tech Stack

| Layer | Technology |
|---|---|
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM | Groq (llama3-8b-8192) |
| Framework | LangChain |
| Frontend | Streamlit |
| Containerization | Docker |
| Testing | Pytest |

---

## Architecture

```text
PDF
 ↓
Loader
 ↓
Chunker
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Retriever
 ↓
Groq LLM
 ↓
Answer + Sources
```

---

## Project Structure

```text
rag-brain/
├── src/
│   └── rag_brain/
│       ├── ingestion/
│       ├── retrieval/
│       ├── generation/
│       ├── config.py
│       └── pipeline.py
│
├── app/
│   └── streamlit_app.py
│
├── tests/
│
├── data/docs/
├── vectorstore/
├── assets/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Local Setup

```bash
git clone <repo-url>

cd rag-brain

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
copy .env.example .env
```

Add:

```env
GROQ_API_KEY=your_key
```

Run:

```bash
streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## Docker

Build and run:

```bash
docker compose up --build
```

---

## Run Tests

```bash
pytest tests/ -v
```

Current status:

```text
11/11 tests passing
```

---

## Environment Variables

| Variable | Purpose |
|---|---|
| GROQ_API_KEY | Groq API access |
| EMBEDDING_MODEL | Embedding model |
| LLM_MODEL | LLM model |
| CHROMA_PERSIST_DIR | Chroma storage path |
| CHUNK_SIZE | Chunk size |
| CHUNK_OVERLAP | Chunk overlap |
| TOP_K | Number of retrieved chunks |

---

## CI/CD

GitHub Actions:

- runs tests automatically
- validates code on push
- builds Docker image
- blocks broken builds

---

## Future Improvements

- Multi-PDF support
- Separate collections per document
- Citation highlighting
- Authentication
- Deployment support
- Conversation memory
