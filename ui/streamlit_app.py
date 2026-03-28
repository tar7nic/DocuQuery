import streamlit as st
import os 
import tempfile
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)
from app.rag_pipeline import ingest_pdf, ask

st.set_page_config(page_title="DocuQuery", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Change accent color from red to cyan */
    :root {
        --primary-color: #00b4d8;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        border-right: 1px solid #2d2f3e;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 4px 8px;
        margin-bottom: 8px;
    }
    
    /* Input box */
    [data-testid="stChatInputTextArea"] {
        border-radius: 12px;
    }

    /* Expander */
    [data-testid="stExpander"] {
        border-radius: 8px;
        border: 1px solid #2d2f3e !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
    
if "answer_length" not in st.session_state:
    st.session_state.answer_length = "Balanced"

# Welcome screen
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <h1>Welcome to DocuQuery</h1>
            <p style='color: #8b8fa8; font-size: 16px;'>
                Upload a PDF from the sidebar and ask anything.<br>
                Get precise answers with source citations.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# ⚡ DocuQuery")
    st.markdown("<p style='color: #8b8fa8; font-size: 13px;'>RAG-powered PDF assistant</p>", unsafe_allow_html=True)
    st.divider()
    
    uploaded_files = st.file_uploader(
        "Upload PDF files", accept_multiple_files=True, type="pdf"
    )
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.uploaded_docs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            ingest_pdf(tmp_path, uploaded_file.name)
            os.unlink(tmp_path)
            st.session_state.uploaded_docs.append(uploaded_file.name)
            st.rerun()
    
    st.divider()
    st.markdown("**⚙️ Response Settings**")
    st.session_state.answer_length = st.select_slider(
        "Answer Length",
        options=["Short", "Balanced", "Detailed"],
        value="Balanced"
    )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message and len(message["sources"]) > 0:
            with st.expander(f"📎 {len(message['sources'])} sources cited"):
                for s in message["sources"]:
                    st.markdown(f"**{s['filename']}**")
                    if str(s['page']).startswith('http'):  # web source
                        st.markdown(f"🌐 [{s['page']}]({s['page']})")
                    else:  # PDF source
                        st.markdown(f"📄 Page {s['page']}")
                    st.caption(s["snippet"])

# Handle new question
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if not st.session_state.uploaded_docs:
        # No PDF uploaded — go straight to web search
        from app.generator import web_search_answer
        result = web_search_answer(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })
        st.rerun()
    
    else:
        result = ask(prompt, st.session_state.answer_length)
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })
        st.rerun()