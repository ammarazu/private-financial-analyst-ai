import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from langfuse import Langfuse
from datetime import datetime

lf = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host="https://cloud.langfuse.com"
)

def track_query(question: str, answer: str, chunks: list, model: str = "gpt-4o-mini"):
    trace_id = lf.create_trace_id()
    lf.set_current_trace_io(input=question, output=answer)
    lf.flush()
    print(f"   📊 Tracked in Langfuse! ID: {trace_id[:8]}")
    return trace_id

if __name__ == "__main__":
    print("Testing Langfuse cost tracker...")
    track_query(
        question="What is this project about?",
        answer="This is a Private Financial Analyst AI system.",
        chunks=[{"source": "project_spec.md", "text": "test"}],
    )
    print("✅ Done! Check cloud.langfuse.com")
