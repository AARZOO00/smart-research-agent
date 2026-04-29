"""
╔══════════════════════════════════════════════════╗
║         SMART RESEARCH AGENT — app.py            ║
║  A multi-step AI agent that plans, searches,     ║
║  and summarizes research on any topic.           ║
╚══════════════════════════════════════════════════╝

HOW THE AGENT WORKS (high-level):
  Step 1 — PLAN   : Break the topic into 4–5 sub-questions
  Step 2 — SEARCH : Answer each sub-question with AI
  Step 3 — REPORT : Synthesize everything into a final report

REQUIREMENTS:
  pip install streamlit huggingface_hub

RUN:
  streamlit run app.py

API KEY:
  Get your FREE Hugging Face token at → https://huggingface.co/settings/tokens
  Click "New token" → Role: "Read" → Copy it → paste in the sidebar.
"""

# ── Standard library ──────────────────────────────────────────────────────────
import time

# ── Third-party ───────────────────────────────────────────────────────────────
import streamlit as st
from huggingface_hub import InferenceClient  # pip install huggingface_hub

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the very first Streamlit call)
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Smart Research Agent",
    page_icon="🔬",
    layout="wide",
)

# ── Model to use — free on Hugging Face Inference API ─────────────────────────
# Mistral-7B is fast, free, and great for structured research tasks.
HF_MODEL = "Qwen/Qwen2.5-72B-Instruct"
# Auto-detect: deployed app pe secrets se, local pe sidebar se
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
    KEY_FROM_SECRETS = True
except Exception:
    HF_API_KEY = None
    KEY_FROM_SECRETS = False

# ═════════════════════════════════════════════════════════════════════════════
#  CUSTOM CSS  — clean, readable, beginner-friendly dark-accent theme
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* ── Header banner ── */
    .hero {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    .hero h1  { font-size: 2rem; font-weight: 600; margin: 0 0 .4rem; }
    .hero p   { font-size: 1rem; opacity: .75;  margin: 0; }

    /* ── Step badges ── */
    .step-badge {
        display: inline-block;
        background: #2c5364;
        color: #7ecfff;
        font-family: 'IBM Plex Mono', monospace;
        font-size: .75rem;
        padding: .2rem .65rem;
        border-radius: 20px;
        margin-bottom: .4rem;
        letter-spacing: .05em;
    }

    /* ── Sub-question cards ── */
    .sq-card {
        background: #f8fafc;
        border-left: 4px solid #2c5364;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: .8rem;
    }
    .sq-title { font-weight: 600; margin-bottom: .3rem; color: #1a2a35; }
    .sq-body  { font-size: .92rem; color: #444; line-height: 1.6; }

    /* ── Final report box ── */
    .report-box {
        background: #fff;
        border: 2px solid #2c5364;
        border-radius: 10px;
        padding: 1.8rem 2rem;
        line-height: 1.8;
    }

    /* ── Progress label ── */
    .prog-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: .8rem;
        color: #888;
        margin-top: .3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
#  HERO HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="hero">
        <h1>🔬 Smart Research Agent</h1>
        <p>Enter any topic → the agent plans sub-questions, researches each one,
           then writes a structured report — all automatically.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — API KEY + SETTINGS
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Settings")

    # ── API Key: Auto from secrets (deployed) OR manual input (local) ───────────
    if KEY_FROM_SECRETS:
        # Deployed app — key already loaded from Streamlit secrets
        api_key = HF_API_KEY
        st.success("🔐 API Key loaded automatically!", icon="✅")
    else:
        # Local run — user enters key manually
        api_key = st.text_input(
            "🤗 Hugging Face Token",
            type="password",
            placeholder="hf_...",
            help="Get free token at: huggingface.co/settings/tokens",
        )
        st.info("🆓 Token is FREE at huggingface.co/settings/tokens", icon="ℹ️")

    st.markdown("---")

    # ── Number of sub-questions the agent should generate ────────────────────
    num_questions = st.slider(
        "Sub-questions to generate",
        min_value=3,
        max_value=6,
        value=4,
        help="More questions → richer report, but slower.",
    )

    st.markdown("---")
    st.caption(
        "**How it works:**\n\n"
        "1. 🗺️ **Plan** — Break topic into sub-questions\n"
        "2. 🔍 **Research** — Answer each sub-question\n"
        "3. 📝 **Report** — Synthesise final output\n\n"
        f"**Model:** `{HF_MODEL}`"
    )

# ═════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
#  Each function calls the Hugging Face Inference API via InferenceClient.
# ═════════════════════════════════════════════════════════════════════════════

def get_client(key: str) -> InferenceClient:
    """Return an authenticated Hugging Face InferenceClient."""
    return InferenceClient(api_key=HF_API_KEY)  # Hardcoded key use ho rahi hai


def call_hf(client: InferenceClient, system: str, user: str) -> str:
    """
    Low-level helper — sends one chat message to Mistral-7B on Hugging Face
    and returns the reply as a plain string.

    Parameters
    ----------
    client  : authenticated HF InferenceClient
    system  : system prompt (sets the model's role / behaviour)
    user    : the actual user message / task

    Returns
    -------
    str — the model's plain-text reply
    """
    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


# ── STEP 1 · PLAN ─────────────────────────────────────────────────────────────

def plan_sub_questions(client, topic: str, n: int) -> list[str]:
    """
    Ask the model to decompose the research topic into `n` focused sub-questions.
    Returns a Python list of question strings.
    """
    system = (
        "You are a research planning assistant. "
        "When given a topic, output ONLY a numbered list of sub-questions "
        "that together provide comprehensive coverage of that topic. "
        "No preamble, no explanation — just the numbered list."
    )
    user = (
        f"Topic: {topic}\n\n"
        f"Generate exactly {n} focused sub-questions that together cover this topic well."
    )

    raw = call_hf(client, system, user)

    # Parse "1. Question?" → ["Question?", ...]
    questions = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip common list prefixes
        for prefix in ["1.","2.","3.","4.","5.","6.","1)","2)","3)","4)","5)","6)","-","*","•"]:
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
                break
        if line:
            questions.append(line)

    # Safety fallback
    if not questions:
        questions = [l.strip() for l in raw.splitlines() if l.strip()]

    return questions[:n]


# ── STEP 2 · RESEARCH ─────────────────────────────────────────────────────────

def research_sub_question(client, topic: str, question: str) -> str:
    """
    Ask the model to answer one sub-question in the context of the broader topic.
    Returns 2–3 paragraphs of detailed text.
    """
    system = (
        "You are an expert research assistant with deep knowledge across many domains. "
        "Answer the given research question clearly, accurately, and concisely. "
        "Write 2–3 well-structured paragraphs. Use plain English. No bullet points."
    )
    user = (
        f"Overall research topic: {topic}\n\n"
        f"Specific sub-question to answer: {question}"
    )
    return call_hf(client, system, user)


# ── STEP 3 · REPORT ───────────────────────────────────────────────────────────

def generate_final_report(client, topic: str, qa_pairs: list[dict]) -> str:
    """
    Synthesise all sub-question answers into one structured Markdown report.
    `qa_pairs` is a list of {"question": ..., "answer": ...} dicts.
    """
    context = "\n\n".join(
        f"Q: {item['question']}\nA: {item['answer']}"
        for item in qa_pairs
    )

    system = (
        "You are a professional research writer. "
        "Given a research topic and a set of Q&A findings, "
        "write a well-structured report using Markdown. "
        "Include: an Executive Summary, clearly labelled sections for each finding, "
        "and a concise Conclusion. Keep it under 600 words total."
    )
    user = (
        f"Research Topic: {topic}\n\n"
        f"Research Findings:\n{context}\n\n"
        "Write the full structured report now."
    )
    return call_hf(client, system, user)


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN UI  — Input + Run button
# ═════════════════════════════════════════════════════════════════════════════

topic = st.text_input(
    "📌 Research Topic",
    placeholder="e.g. The impact of quantum computing on cybersecurity",
    help="Enter any topic you want to research.",
)

run_button = st.button("🚀 Run Research Agent", type="primary", use_container_width=True)

# ── Guard: nothing runs until the button is clicked ──────────────────────────
if run_button:

    # ── Validate inputs ──────────────────────────────────────────────────────
    if not topic.strip():
        st.error("⚠️ Please enter a research topic before running the agent.")
        st.stop()

    if not KEY_FROM_SECRETS and not api_key.strip():
        st.error("⚠️ Please enter your Hugging Face token in the sidebar.")
        st.stop()

    # ── Initialise client ────────────────────────────────────────────────────
    try:
        client = get_client(api_key)
    except Exception as e:
        st.error(f"Could not create API client: {e}")
        st.stop()

    # ════════════════════════════════════════════════════════════════════════
    #  STEP 1 — PLAN
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="step-badge">STEP 1 · PLAN</span>', unsafe_allow_html=True)
    st.subheader("🗺️ Breaking topic into sub-questions…")

    with st.spinner("Planning research structure…"):
        try:
            questions = plan_sub_questions(client, topic, num_questions)
        except Exception as e:
            st.error(f"Planning step failed: {e}")
            st.stop()

    # Display the plan as a checklist
    st.success(f"✅ Generated {len(questions)} sub-questions")
    for i, q in enumerate(questions, 1):
        st.markdown(f"**{i}.** {q}")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    #  STEP 2 — RESEARCH  (iterate over every sub-question)
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="step-badge">STEP 2 · RESEARCH</span>', unsafe_allow_html=True)
    st.subheader("🔍 Researching each sub-question…")

    # Progress bar tracks completion across all questions
    progress_bar   = st.progress(0)
    progress_label = st.empty()   # Will show "Researching 2 / 4…" text

    qa_pairs = []  # Will hold {"question": ..., "answer": ...} for each item

    for idx, question in enumerate(questions):
        # Update the progress UI
        fraction = idx / len(questions)
        progress_bar.progress(fraction)
        progress_label.markdown(
            f'<p class="prog-label">Researching {idx + 1} / {len(questions)}: {question}</p>',
            unsafe_allow_html=True,
        )

        # Call the research function
        try:
            answer = research_sub_question(client, topic, question)
        except Exception as e:
            answer = f"⚠️ Could not retrieve answer: {e}"

        qa_pairs.append({"question": question, "answer": answer})

        # Render the completed card immediately (streaming feel)
        st.markdown(
            f"""
            <div class="sq-card">
                <div class="sq-title">Q{idx + 1}: {question}</div>
                <div class="sq-body">{answer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Small delay so the UI updates feel progressive, not all-at-once
        time.sleep(0.2)

    # Mark progress complete
    progress_bar.progress(1.0)
    progress_label.markdown(
        '<p class="prog-label">✅ All sub-questions answered</p>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    #  STEP 3 — REPORT
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="step-badge">STEP 3 · REPORT</span>', unsafe_allow_html=True)
    st.subheader("📝 Generating Final Report…")

    with st.spinner("Synthesising findings into a structured report…"):
        try:
            report = generate_final_report(client, topic, qa_pairs)
        except Exception as e:
            st.error(f"Report generation failed: {e}")
            st.stop()

    st.success("✅ Report ready!")

    # ── Render the report inside a styled box ────────────────────────────────
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(report)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Download button — save the report as a .md file ──────────────────────
    st.download_button(
        label="⬇️ Download Report (.md)",
        data=report,
        file_name=f"research_report_{topic[:30].replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Smart Research Agent · Built with Streamlit + Anthropic Claude · Plan → Research → Report")