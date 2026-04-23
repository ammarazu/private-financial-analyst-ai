import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# ── CONFIG ──────────────────────────────────────────────
CHROMA_DIR = Path(__file__).parent.parent / "infrastructure" / "chroma_db"
COLLECTION_NAME = "financial_docs"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOP_K = 3  # how many chunks to retrieve

client_openai = OpenAI(api_key=OPENAI_API_KEY)

# ── SETUP CHROMADB ───────────────────────────────────────
def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

# ── STEP 1: SEARCH ───────────────────────────────────────
def search_documents(question: str, collection) -> list[dict]:
    """Find most relevant chunks for the question"""
    print(f"\n🔍 Searching for: '{question}'")
    results = collection.query(
        query_texts=[question],
        n_results=TOP_K
    )
    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text": doc,
            "source": results["metadatas"][0][i]["source"],
            "chunk_num": results["metadatas"][0][i]["chunk_num"]
        })
        print(f"   📄 Chunk {i+1}: {doc[:80]}...")
    return chunks

# ── STEP 2: BUILD PROMPT ─────────────────────────────────
def build_prompt(question: str, chunks: list[dict]) -> str:
    """Combine retrieved chunks into a prompt"""
    context = "\n\n".join([
        f"[Source: {c['source']} | Chunk {c['chunk_num']}]\n{c['text']}"
        for c in chunks
    ])
    return f"""You are a Private Financial Analyst AI assistant.
Answer the question based ONLY on the context provided below.
If the answer is not in the context, say "I don't have that information in the documents."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

# ── STEP 3: ASK GPT ──────────────────────────────────────
def ask_gpt(prompt: str) -> str:
    """Send prompt to GPT-4o-mini and get answer"""
    print("🤖 Asking GPT-4o-mini...")
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content

# ── MAIN QUERY FUNCTION ──────────────────────────────────
def query(question: str) -> dict:
    """Full RAG query pipeline"""
    collection = get_collection()
    chunks = search_documents(question, collection)
    from reranker import rerank
    chunks = rerank(question, chunks, top_n=3)
    prompt = build_prompt(question, chunks)
    answer = ask_gpt(prompt)
    return {
        "question": question,
        "answer": answer,
        "sources": [c["source"] for c in chunks]
    }

# ── INTERACTIVE MODE ─────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*50)
    print("💼 PRIVATE FINANCIAL ANALYST AI - Day 24")
    print("="*50)
    print("Type your question (or 'quit' to exit)\n")

    collection = get_collection()
    print(f"📦 Loaded collection: {COLLECTION_NAME}")
    print(f"   Documents in DB: {collection.count()}\n")

    while True:
        question = input("❓ Your question: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue

        result = query(question)
        print(f"\n{'─'*50}")
        print(f"💡 ANSWER:\n{result['answer']}")
        print(f"\n📚 Sources: {', '.join(set(result['sources']))}")
        print(f"{'─'*50}\n")
