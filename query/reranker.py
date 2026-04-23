import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

import cohere

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def rerank(question: str, chunks: list[dict], top_n: int = 3) -> list[dict]:
    """Rerank chunks by relevance to question using Cohere"""
    print(f"🎯 Reranking {len(chunks)} chunks...")

    if not chunks:
        return chunks

    # Rerank using Cohere
    docs = [c["text"] for c in chunks]
    results = co.rerank(
        query=question,
        documents=docs,
        top_n=top_n,
        model="rerank-english-v3.0"
    )

    # Rebuild chunks in reranked order
    reranked = []
    for r in results.results:
        chunk = chunks[r.index].copy()
        chunk["relevance_score"] = round(r.relevance_score, 4)
        reranked.append(chunk)
        print(f"   📊 Score {chunk['relevance_score']} → {chunk['text'][:60]}...")

    print(f"   ✅ Top {top_n} chunks selected")
    return reranked

if __name__ == "__main__":
    # Test reranker
    test_chunks = [
        {"text": "The project uses AWS Bedrock for LLM routing.", "source": "doc1", "chunk_num": 0},
        {"text": "Security measures include PII stripping with Presidio.", "source": "doc1", "chunk_num": 1},
        {"text": "The system supports PDF and SEC filings.", "source": "doc1", "chunk_num": 2},
        {"text": "Cohere Rerank improves search quality significantly.", "source": "doc1", "chunk_num": 3},
        {"text": "Terraform is used for infrastructure deployment.", "source": "doc1", "chunk_num": 4},
    ]

    question = "What security features are in the system?"
    print(f"Question: {question}\n")
    results = rerank(question, test_chunks, top_n=3)
    print("\nFinal ranking:")
    for i, r in enumerate(results):
        print(f"  {i+1}. [{r['relevance_score']}] {r['text']}")
