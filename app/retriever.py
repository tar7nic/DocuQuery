from app.embeddings import embed_texts
from app.vectorstore import search,get_client
from sentence_transformers import CrossEncoder


def retrieve(query: str, top_k=10) -> list[dict]:
    client = get_client()
    query_vector = embed_texts([query])[0]
    results = search(client,query_vector,top_k)
    return results

def rerank(query: str, results: list, top_n=4) -> list[dict]:
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
    pairs = [[query, result.payload["text"]] for result in results]
    scores = model.predict(pairs)
    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return [result for result, score in ranked[:top_n]]
    
if __name__ == "__main__":
    results = retrieve("what is the job description?")
    reranked = rerank("what is the job description?", results)
    for r in reranked:
        print(r.payload["filename"], "Page", r.payload["page"])
        print(r.payload["text"][:150])
        print("---")