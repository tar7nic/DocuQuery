import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingest import process_pdf
from app.embeddings import embed_texts
from app.vectorstore import get_client, upsert_chunks,create_collection
from app.retriever import retrieve, rerank
from app.generator import generate_answer

def ingest_pdf(filepath: str, filename: str = None):
    chunks = process_pdf(filepath)
    print(f"Total chunks created: {len(chunks)}")
    
    if filename:
        for chunk in chunks:
            chunk["filename"] = filename
    
    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts)
    print(f"Total vectors created: {len(vectors)}")
    
    client = get_client()
    create_collection(client)
    upsert_chunks(client, chunks, vectors)
    print(f"Done! Ingested {len(chunks)} chunks")

def ask(question: str, answer_length: str = "Balanced") -> dict:
    s1op = retrieve(question, 10)
    s2op = rerank(question, s1op, 4)
    result = generate_answer(question, s2op, answer_length)
    return result

if __name__ == "__main__":
    ingest_pdf("testdata/Machine learning.pdf", "Machine learning.pdf")