import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent / ".env")

import chromadb
from chromadb.utils import embedding_functions
from unstructured.partition.auto import partition
from unstructured.cleaners.core import clean

# ── CONFIG ──────────────────────────────────────────────
DOCS_DIR = Path(__file__).parent.parent / "documents"
CHROMA_DIR = Path(__file__).parent.parent / "infrastructure" / "chroma_db"
COLLECTION_NAME = "financial_docs"
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 50     # overlap between chunks

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ── STEP 1: LOAD ────────────────────────────────────────
def load_document(filepath: Path) -> str:
    """Load any document type using unstructured"""
    print(f"📄 Loading: {filepath.name}")
    elements = partition(filename=str(filepath))
    # Join all elements into one text block
    raw_text = "\n".join([str(el) for el in elements])
    print(f"   ✅ Loaded {len(elements)} elements, {len(raw_text)} chars")
    return raw_text

# ── STEP 2: CLEAN ───────────────────────────────────────
def clean_text(text: str) -> str:
    """Remove extra whitespace, fix encoding issues"""
    print("🧹 Cleaning text...")
    cleaned = clean(text, extra_whitespace=True, dashes=True, bullets=True)
    print(f"   ✅ Cleaned: {len(cleaned)} chars")
    return cleaned

# ── STEP 3: CHUNK ───────────────────────────────────────
def chunk_text(text: str, source: str) -> list[dict]:
    """Split text into overlapping chunks with metadata"""
    print(f"✂️  Chunking into {CHUNK_SIZE}-char pieces...")
    chunks = []
    start = 0
    chunk_num = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text_content = text[start:end]

        # Don't save tiny leftover chunks
        if len(chunk_text_content.strip()) > 50:
            chunks.append({
                "text": chunk_text_content,
                "metadata": {
                    "source": source,
                    "chunk_num": chunk_num,
                    "start_char": start,
                    "end_char": end
                }
            })
            chunk_num += 1

        start += CHUNK_SIZE - CHUNK_OVERLAP  # overlap

    print(f"   ✅ Created {len(chunks)} chunks")
    return chunks

# ── STEP 4+5: EMBED & STORE ─────────────────────────────
def embed_and_store(chunks: list[dict], collection):
    """Embed chunks using OpenAI and store in ChromaDB"""
    print(f"🧠 Embedding and storing {len(chunks)} chunks...")

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"{c['metadata']['source']}_chunk_{c['metadata']['chunk_num']}" for c in chunks]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    print(f"   ✅ Stored in ChromaDB!")

# ── MAIN PIPELINE ───────────────────────────────────────
def run_pipeline():
    print("\n" + "="*50)
    print("🚀 DOCUMENT INGESTION PIPELINE - Day 23")
    print("="*50 + "\n")

    # Setup ChromaDB
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Setup embedding function (OpenAI)
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )

    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )
    print(f"📦 ChromaDB collection: '{COLLECTION_NAME}'")
    print(f"   Current docs in DB: {collection.count()}\n")

    # Process all documents
    doc_files = list(DOCS_DIR.glob("*"))
    if not doc_files:
        print("❌ No documents found in documents/ folder!")
        return

    total_chunks = 0
    for filepath in doc_files:
        if filepath.suffix in ['.py', '.db']:
            continue
        print(f"\n{'─'*40}")
        raw = load_document(filepath)
        cleaned = clean_text(raw)
        from pii_stripper import strip_pii
        pii_result = strip_pii(cleaned)
        cleaned = pii_result["clean_text"]
        print(f"   PII items removed: {pii_result["count"]}")
        chunks = chunk_text(cleaned, filepath.name)
        embed_and_store(chunks, collection)
        total_chunks += len(chunks)

    print(f"\n{'='*50}")
    print(f"✅ PIPELINE COMPLETE!")
    print(f"   Total chunks stored: {total_chunks}")
    print(f"   Total docs in DB: {collection.count()}")
    print(f"   DB location: {CHROMA_DIR}")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()
