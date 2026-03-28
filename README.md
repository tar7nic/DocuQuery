# DocuQuery ⚡
> AI-powered PDF question answering using RAG — ask anything from your documents and get precise answers with source citations.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-purple)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-green)

---

## 🧠 What is DocuQuery?

DocuQuery is an AI-powered document assistant that lets you upload any PDF and ask questions about it in plain English. It uses a full **Retrieval-Augmented Generation (RAG)** pipeline to find the most relevant information and generate accurate, cited answers.

---

## 🏗️ Architecture

```
PDF Upload → Text Extraction → Chunking → Embedding
                                              ↓
User Question → Query Embedding → Qdrant Search (Top 10)
                                              ↓
                              Cross-Encoder Re-ranking (Top 4)
                                              ↓
                              Groq LLM (LLaMA 3.1) → Answer + Citations
```

---

## ✨ Features

- 📄 Upload multiple PDFs and query across all of them
- 🔍 Semantic search using sentence-transformers embeddings
- 🎯 Cross-encoder re-ranking for high precision retrieval
- 💬 Cited answers with filename and page number
- ⚡ Fast inference via Groq API
- 🎛️ Dynamic answer length — Short, Balanced, or Detailed

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| PDF Parsing | PyMuPDF |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | Qdrant Cloud |
| Re-ranking | CrossEncoder (ms-marco-MiniLM-L-6-v2) |
| LLM | Groq API (LLaMA 3.1 8B) |
| UI | Streamlit |

---

## 🚀 Running Locally

**1. Clone the repo:**
```bash
git clone https://github.com/tar7nic/DocuQuery.git
cd DocuQuery
```

**2. Create a virtual environment:**
```bash
conda create -n RAGenv python=3.11
conda activate RAGenv
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

Get your free keys here:
- Groq API: https://console.groq.com
- Qdrant Cloud: https://cloud.qdrant.io

**5. Run the app:**
```bash
streamlit run ui/streamlit_app.py
```

---

## 📁 Project Structure

```
DocuQuery/
│
├── app/
│   ├── ingest.py          # PDF extraction + chunking
│   ├── embeddings.py      # Sentence transformer embeddings
│   ├── vectorstore.py     # Qdrant connection + operations
│   ├── retriever.py       # Query retrieval + re-ranking
│   ├── generator.py       # Groq LLM generation
│   └── rag_pipeline.py    # End-to-end pipeline
│
├── ui/
│   └── streamlit_app.py   # Streamlit frontend
│
├── eval/
│   └── evaluate.py        # RAGAs evaluation
│
├── .streamlit/
│   └── config.toml        # Streamlit theme config
│
├── requirements.txt
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key |
| `QDRANT_URL` | Your Qdrant cluster URL |
| `QDRANT_API_KEY` | Your Qdrant API key |

---

## 👤 Author

Built by [Tronny](https://github.com/tar7nic) as a portfolio project demonstrating end-to-end RAG engineering.
```