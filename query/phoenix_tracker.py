import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

import phoenix as px
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from phoenix.otel import register

def setup_phoenix():
    """Start Phoenix observability server"""
    print("🔭 Starting Arize Phoenix...")
    session = px.launch_app()
    print(f"   ✅ Phoenix running at: {session.url}")
    return session

def trace_query(question: str, chunks: list, answer: str):
    """Trace a complete query"""
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("financial-analyst-query") as span:
        span.set_attribute("question", question)
        span.set_attribute("chunks_retrieved", len(chunks))
        span.set_attribute("answer_length", len(answer))
    print(f"   🔭 Traced in Phoenix!")

if __name__ == "__main__":
    print("Testing Arize Phoenix...")
    session = setup_phoenix()
    print(f"✅ Open browser at: {session.url}")
