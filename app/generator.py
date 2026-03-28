from dotenv import load_dotenv
import os
from groq import Groq
from duckduckgo_search import DDGS

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def generate_answer(query: str, chunks: list, answer_length: str = "Balanced") -> dict:
    
    length_instruction = {
        "Short": "Answer in 2-3 sentences maximum. Be direct and concise.",
        "Balanced": "Answer in a short paragraph. Cover the key points clearly.",
        "Detailed": "Answer in detail with multiple paragraphs. Explain thoroughly with examples from the context."
    }

    system_prompt = f"""You are a precise research assistant.
Answer using ONLY the provided context.
Cite sources inline as [Filename, Page X].
If the context doesn't contain the answer, say so clearly.
When citing, if multiple sources are from the same page, cite that page only once.

Answer length instruction: {length_instruction[answer_length]}"""

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
        f"[{i}] {chunk.payload['filename']}, Page {chunk.payload['page']}:\n{chunk.payload['text']}"
    )
    context = "\n\n".join(context_parts)
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        temperature=0.2
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": [
            {
                "filename": chunk.payload["filename"],
                "page": chunk.payload["page"],
                "snippet": chunk.payload["text"][:200]
            }
            for chunk in chunks
        ]
    }
    
def web_search_answer(query: str) -> dict:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=4))
    
    context = "\n\n".join([
        f"[{i+1}] {r['title']} ({r['href']}):\n{r['body']}"
        for i, r in enumerate(results)
    ])
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": """Answer the question using the web search results provided. 
                    Cite sources inline as [1], [2] etc.
                    Do NOT add a References section at the end — sources will be shown separately."""},
            {"role": "user", "content": f"Search results:\n{context}\n\nQuestion: {query}"}
        ],
        temperature=0.2
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": [
            {
                "filename": r["title"],
                "page": r["href"],
                "snippet": r["body"][:200]
            }
            for r in results
        ]
    }