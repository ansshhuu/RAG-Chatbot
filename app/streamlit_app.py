import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag_brain.pipeline import ingest_pdf, ask_question

st.set_page_config(
    page_title="RAG Chatbot",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ── ROOT ── */
:root {
    --green:       #00ff88;
    --green-dim:   #00cc6a;
    --green-dark:  #003322;
    --green-glow:  rgba(0, 255, 136, 0.15);
    --bg:          #020d07;
    --bg-card:     #050f09;
    --border:      rgba(0, 255, 136, 0.2);
    --text:        #c8fde0;
    --text-dim:    #4a7a5e;
    --mono:        'Share Tech Mono', monospace;
    --sans:        'Rajdhani', sans-serif;
}

/* ── GLOBAL ── */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* scanline overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,136,0.015) 2px,
        rgba(0,255,136,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    max-width: 780px !important;
}

/* ── HEADER ── */
.rag-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.rag-header h1 {
    font-family: var(--mono) !important;
    font-size: 2.8rem !important;
    color: var(--green) !important;
    text-shadow: 0 0 30px rgba(0,255,136,0.5), 0 0 60px rgba(0,255,136,0.2);
    letter-spacing: 0.15em;
    margin: 0 !important;
}
.rag-header p {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--text-dim);
    letter-spacing: 0.2em;
    margin-top: 0.5rem;
    text-transform: uppercase;
}

/* ── STATUS BADGE ── */
.status-bar {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-align: center;
    margin-bottom: 2rem;
}
.status-bar .dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── UPLOAD ZONE ── */
.upload-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--text-dim);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

[data-testid="stFileUploader"] {
    border: 1px dashed var(--border) !important;
    border-radius: 4px !important;
    background: var(--bg-card) !important;
    padding: 1rem !important;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--green) !important;
    box-shadow: 0 0 20px var(--green-glow);
}
[data-testid="stFileUploader"] * {
    color: var(--text-dim) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--green) !important;
    color: var(--green) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.15em !important;
    border-radius: 2px !important;
    padding: 0.5rem 2rem !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--green-glow) !important;
    box-shadow: 0 0 20px var(--green-glow) !important;
}

/* ── ALERTS ── */
.stSuccess, .stInfo, .stWarning {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    color: var(--green) !important;
}

/* ── DIVIDER ── */
.seg-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
    color: var(--text-dim);
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.seg-divider::before, .seg-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    margin-bottom: 0.75rem !important;
    font-family: var(--sans) !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text) !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
}

/* user msg accent */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-color: rgba(0,255,136,0.4) !important;
    background: rgba(0,255,136,0.04) !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    background: var(--bg-card) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--green) !important;
    box-shadow: 0 0 15px var(--green-glow) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-dim) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    background: var(--bg-card) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-dim) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
}

/* spinner */
.stSpinner > div {
    border-top-color: var(--green) !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="rag-header">
    <h1>⬡ RAG Chatbot</h1>
    <p>semantic search · retrieval augmented generation · groq llm</p>
</div>
<div class="status-bar">
    <span class="dot"></span> SYSTEM ONLINE · CHROMADB READY
</div>
""", unsafe_allow_html=True)

if "pdf_ready" not in st.session_state:
    st.session_state["pdf_ready"] = False
if "pdf_name" not in st.session_state:
    st.session_state["pdf_name"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not st.session_state["pdf_ready"]:

    st.markdown('<div class="upload-label">// upload document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="upload",
        type="pdf",
        label_visibility="collapsed"
    )

    if uploaded_file:
        if st.button("Process Document"):
            tmp_path = f"data/docs/{uploaded_file.name}"
            os.makedirs("data/docs", exist_ok=True)

            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.read())

            with st.spinner("PROCESSING..."):
                ingest_pdf(tmp_path)

            st.session_state["pdf_ready"] = True
            st.session_state["pdf_name"] = uploaded_file.name
            st.rerun()


else:
    st.success(f"LOADED — {st.session_state['pdf_name']}")

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("↺ RESET"):
            st.session_state["pdf_ready"] = False
            st.session_state["pdf_name"] = ""
            st.session_state["messages"] = []
            st.rerun()

    st.markdown('<div class="seg-divider">query interface</div>', unsafe_allow_html=True)

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.get("_processing"):
        with st.spinner("GENERATING..."):
            result = ask_question(st.session_state["_pending_q"])
            answer = result["answer"]
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.session_state["_processing"] = False
        st.session_state["_pending_q"] = ""
        st.rerun()

    if question := st.chat_input("ask anything about your document..."):
        st.session_state["messages"].append({"role": "user", "content": question})
        st.session_state["_processing"] = True
        st.session_state["_pending_q"] = question
        st.rerun()
