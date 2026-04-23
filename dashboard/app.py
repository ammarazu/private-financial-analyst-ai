import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from query.query_engine import query

# ── PAGE CONFIG ─────────────────────────────────────────
st.set_page_config(
    page_title="Private Financial Analyst AI",
    page_icon="💼",
    layout="wide"
)

# ── STYLING ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────
st.title("💼 Private Financial Analyst AI")
st.markdown("*Ask questions about your financial documents*")
st.divider()

# ── CHAT HISTORY ────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── INPUT ───────────────────────────────────────────────
if question := st.chat_input("Ask about your financial documents..."):

    # Show user question
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Get answer
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching documents..."):
            result = query(question)

        st.write(result["answer"])
        st.caption(f"📚 Sources: {', '.join(set(result['sources']))}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.header("📊 System Info")
    st.success("✅ ChromaDB Connected")
    st.success("✅ GPT-4o-mini Ready")
    st.divider()
    st.markdown("**Sample Questions:**")
    st.markdown("- What is this project about?")
    st.markdown("- What security measures are used?")
    st.markdown("- What technologies are mentioned?")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
