import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.rag_pipeline import ask
from app.retriever import retrieve, rerank
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from datasets import Dataset

# Judge LLM
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    n=1  
)
judge_llm = LangchainLLMWrapper(groq_llm)

# Local embeddings
local_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

# Test questions
questions = [
    "What is backpropagation?",
    "What are the challenges of neural networks?",
    "How do CNNs work?",
    "What is a perceptron?",
    "What are transformer networks?",
]

# Run pipeline
data = {
    "question": [],
    "answer": [],
    "contexts": [],
}

for q in questions:
    result = ask(q)
    chunks = rerank(q, retrieve(q))
    data["question"].append(q)
    data["answer"].append(result["answer"])
    data["contexts"].append([c.payload["text"] for c in chunks])

# Evaluate
dataset = Dataset.from_dict(data)
scores = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=judge_llm,
    embeddings=local_embeddings,
)

print(scores)