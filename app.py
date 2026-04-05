import streamlit as st
import os
from dotenv import load_dotenv
from agent import ReActAgent

load_dotenv()

st.set_page_config(page_title="ReAct Agent", page_icon="🤖", layout="wide")

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
.thought-box   { background:#1e3a5f; border-left:4px solid #4a9eff; padding:10px 14px; border-radius:6px; margin:6px 0; }
.action-box    { background:#3b2a1a; border-left:4px solid #f0a500; padding:10px 14px; border-radius:6px; margin:6px 0; }
.observe-box   { background:#1a3b2a; border-left:4px solid #2ecc71; padding:10px 14px; border-radius:6px; margin:6px 0; }
.final-box     { background:#2a1a3b; border-left:4px solid #9b59b6; padding:10px 14px; border-radius:6px; margin:6px 0; }
.error-box     { background:#3b1a1a; border-left:4px solid #e74c3c; padding:10px 14px; border-radius:6px; margin:6px 0; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")

    api_key = st.text_input(
        "🔑 Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="Free key at console.groq.com — login with GitHub or Gmail"
    )

    model = st.selectbox("🤖 Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
    ])

    max_iter = st.slider("🔁 Max Iterations", min_value=3, max_value=15, value=8)

    st.divider()
    st.subheader("🔧 Available Tools")
    st.markdown("""
- 🧮 **Calculator** — Safe math eval (no API)
- 🌤️ **Weather** — Open-Meteo (free, no key)
- 🔍 **Web Search** — DuckDuckGo (free, no key)
- 📚 **Wikipedia** — Article summaries (free)
""")

    st.divider()
    st.subheader("💡 Try These Examples")
    examples = [
        "What is sqrt(2025) + log(1000)?",
        "Current weather in Tiruppur and London?",
        "Who invented the transformer architecture in AI?",
        "What is quantum entanglement?",
        "Compound interest: ₹50000 at 7% for 10 years?",
        "Who is the CEO of NVIDIA and what is the company known for?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True, key=ex):
            st.session_state["prefill"] = ex

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["history"] = []
        st.rerun()

# ─── Session State ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state["history"] = []

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🤖 ReAct Agent from Scratch")
st.caption("Built with Groq (Llama 3.3) · Open-Meteo · DuckDuckGo · Wikipedia · Zero paid APIs")

# ─── Display chat history ─────────────────────────────────────────────────────
for entry in st.session_state["history"]:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"], unsafe_allow_html=True)

# ─── Input ────────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill", "")
query = st.chat_input("Ask anything...", key="chat_input") or prefill

if query:
    if not api_key:
        st.warning("⚠️ Add your Groq API Key in the sidebar. Get one free at [console.groq.com](https://console.groq.com/keys).")
        st.stop()

    # Show user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state["history"].append({"role": "user", "content": query})

    # Run agent
    with st.chat_message("assistant"):
        trace_placeholder = st.empty()
        trace_html = ""
        final_answer = None

        agent = ReActAgent(api_key=api_key, model=model, max_iterations=max_iter)

        for step in agent.run(query):
            t = step["type"]
            c = step["content"]
            n = step["step"]

            if t == "thought":
                trace_html += f'<div class="thought-box">💭 <b>Thought {n}:</b> {c}</div>'
            elif t == "action":
                trace_html += f'<div class="action-box">⚡ <b>Action {n}:</b> {c}</div>'
            elif t == "observation":
                trace_html += f'<div class="observe-box">👀 <b>Observation {n}:</b><pre style="margin:4px 0">{c}</pre></div>'
            elif t == "final":
                final_answer = c
            elif t == "error":
                trace_html += f'<div class="error-box">⚠️ <b>Error:</b> {c}</div>'

            trace_placeholder.markdown(trace_html, unsafe_allow_html=True)

        if final_answer:
            st.markdown(f'<div class="final-box">✅ <b>Final Answer:</b><br>{final_answer}</div>', unsafe_allow_html=True)
            full = trace_html + f'<div class="final-box">✅ <b>Final Answer:</b><br>{final_answer}</div>'
        else:
            full = trace_html

    st.session_state["history"].append({"role": "assistant", "content": full})