import sys
from pathlib import Path

import streamlit as st
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from rag_brain.pipeline import ingest_pdf,ask_question

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="",
    layout="wide"
)
st.title(" RAG Chatbot")
st.caption("Chat with your PDF using AI")
st.divider()
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file:
        if st.button("Process PDF", use_container_width=True):
            with st.spinner("Processing..."):
                docs_dir = Path("data/docs")
                docs_dir.mkdir(parents=True, exist_ok=True)

                file_path = docs_dir / uploaded_file.name

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                chunk_count = ingest_pdf(str(file_path))

                st.session_state["pdf_ready"] = True
                st.session_state["pdf_name"] = uploaded_file.name
                st.session_state["messages"] = []

            st.success(f"{chunk_count} chunks stored.")

    if st.session_state.get("pdf_ready"):
        st.info(f"Active PDF: {st.session_state['pdf_name']}")

    st.divider()
    st.caption("Built with LangChain · Groq · ChromaDB · Streamlit")


if "messages" not in st.session_state:
    st.session_state["messages"] = []


for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


question = st.chat_input("Ask a question about your document...")

if question:
    if not st.session_state.get("pdf_ready"):
        st.warning("Upload and process a PDF first.")
    else:
        st.session_state["messages"].append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask_question(question)
                answer = result["answer"]
                sources = result["sources"]

            st.markdown(answer)

            with st.expander("Source chunks used"):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"**Chunk {i}:**")
                    st.caption(source)

        st.session_state["messages"].append(
            {"role": "assistant", "content": answer}
        )