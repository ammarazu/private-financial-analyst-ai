import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

eval_data = {
    "question": [
        "What is this project about?",
        "What security features are used?",
        "What technologies are used?"
    ],
    "answer": [
        "This project is about developing a Private Financial Analyst AI system that processes financial documents.",
        "Security features include PII stripping with Presidio, prompt injection blocking, and AWS Secrets Manager.",
        "Technologies include Unstructured.io, ChromaDB, OpenAI, Cohere Rerank, and Langfuse."
    ],
    "contexts": [
        ["Project Specification - Private Financial Analyst AI System. Processes annual reports and SEC filings."],
        ["PII detection and removal via Microsoft Presidio. Prompt injection protection via LLM Guard. Secrets stored in AWS Secrets Manager."],
        ["Vector Database: Weaviate. Embeddings: HuggingFace. Reranking: Cohere Rerank. Cost Tracking: Langfuse."]
    ],
    "ground_truth": [
        "A Private Financial Analyst AI that processes financial documents.",
        "PII stripping, prompt injection protection, and secrets management.",
        "Unstructured.io, ChromaDB, OpenAI, Cohere, and Langfuse."
    ]
}

def get_score(results, key):
    val = results[key]
    if isinstance(val, list):
        valid = [v for v in val if v is not None]
        return sum(valid) / len(valid) if valid else 0.0
    return float(val) if val else 0.0

def run_evaluation():
    print("\n" + "="*50)
    print("📊 RAGAS EVALUATION - Day 28")
    print("="*50 + "\n")

    dataset = Dataset.from_dict(eval_data)
    print("🔍 Running evaluation on 3 test questions...\n")

    results = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision]
    )

    f = get_score(results, 'faithfulness')
    a = get_score(results, 'answer_relevancy')
    c = get_score(results, 'context_precision')

    print("\n" + "="*50)
    print("📈 EVALUATION RESULTS:")
    print("="*50)
    print(f"Faithfulness:      {f:.3f} (target > 0.75)")
    print(f"Answer Relevancy:  {a:.3f} (target > 0.80)")
    print(f"Context Precision: {c:.3f} (target > 0.70)")
    print("="*50)

    passed = 0
    passed += 1 if f > 0.75 else 0
    passed += 1 if a > 0.80 else 0
    passed += 1 if c > 0.70 else 0

    print(f"✅ PASSED" if f > 0.75 else f"❌ FAILED - Faithfulness: {f:.3f}")
    print(f"✅ PASSED" if a > 0.80 else f"❌ FAILED - Answer Relevancy: {a:.3f}")
    print(f"✅ PASSED" if c > 0.70 else f"❌ FAILED - Context Precision: {c:.3f}")
    print(f"\n🎯 Score: {passed}/3 targets met")

if __name__ == "__main__":
    run_evaluation()
