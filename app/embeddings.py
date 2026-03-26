from sentence_transformers import SentenceTransformer as st
 
model = st("all-MiniLM-L6-v2") 

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts)
    return embeddings.tolist()

if __name__ == "__main__":
    results = embed_texts(["hello world", "RAG is cool"])
    print(f"Number of vectors: {len(results)}")
    print(f"Vector size: {len(results[0])}") 
    