# 🔬 Smart Research Agent

> An AI-powered multi-step research agent that **plans**, **researches**, and **reports** — automatically.

---

## 📦 Project Structure

```
smart_research_agent/
├── app.py          ← Single-file Streamlit application (everything lives here)
└── README.md       ← This file
```

---

## ⚡ Quickstart (Run in 3 Steps)

### Step 1 — Install dependencies

```bash
pip install streamlit anthropic
```

### Step 2 — Run the app

```bash
streamlit run app.py
```

### Step 3 — Open in your browser

Streamlit auto-opens at → **http://localhost:8501**

Enter your Anthropic API key in the sidebar (get one free at https://console.anthropic.com), type a topic, and click **Run Research Agent**.

---

## 🔑 Getting Your API Key (Free)

1. Go to **https://console.anthropic.com**
2. Create a free account
3. Navigate to **API Keys** → click **Create Key**
4. Copy and paste it into the app's sidebar

> Free tier gives you generous credits to test the app.

---

## 🧠 How the Agent Works — Step by Step

The agent follows a 3-phase workflow inspired by real research methodology:

```
User Input (topic)
       │
       ▼
┌─────────────┐
│  STEP 1     │  PLAN
│  plan_sub_  │  Ask Claude: "Break this topic into N focused sub-questions"
│  questions()│  → returns ["What is X?", "How does X work?", ...]
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  STEP 2     │  RESEARCH  (loop — one API call per question)
│  research_  │  Ask Claude: "Answer this specific sub-question in depth"
│  sub_       │  → builds qa_pairs = [{"question":..., "answer":...}, ...]
│  question() │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  STEP 3     │  REPORT
│  generate_  │  Ask Claude: "Synthesise all findings into a structured report"
│  final_     │  → returns a Markdown report with sections + conclusion
│  report()   │
└─────────────┘
```

---

## 🗂️ Code Walkthrough — Every Function Explained

### `get_client(key)`
Creates an authenticated Anthropic SDK client. Nothing fancy — just wraps `anthropic.Anthropic(api_key=key)` so the rest of the code stays clean.

---

### `call_claude(client, system, user, model)`
**The core building block** — every AI call goes through here.

| Parameter | What it does |
|-----------|--------------|
| `system`  | Sets Claude's *role* (e.g. "You are a research planner…") |
| `user`    | The actual question / task you're sending |
| `model`   | Which Claude model to use (Sonnet = fast+smart, Haiku = fastest) |

Returns: a plain Python string with Claude's reply.

---

### `plan_sub_questions(client, topic, n, model)`
**STEP 1 — PLAN**

Sends this system prompt:
> "Output ONLY a numbered list of N sub-questions that cover this topic."

Then parses the numbered list into a Python `list[str]`.

Why this works: forcing Claude to output *only* a list (no preamble) makes parsing trivial.

---

### `research_sub_question(client, topic, question, model)`
**STEP 2 — RESEARCH**

Called once per sub-question in a `for` loop.

System prompt sets Claude as an "expert research assistant" and asks for 2–3 solid paragraphs.

The `topic` is passed as context so answers stay relevant to the broader subject.

---

### `generate_final_report(client, topic, qa_pairs, model)`
**STEP 3 — REPORT**

Builds a context string from all Q&A pairs, then asks Claude to write a structured Markdown report with:
- Executive Summary
- One section per finding
- Conclusion

---

## 🎛️ Sidebar Settings

| Setting | What it controls |
|---------|-----------------|
| **API Key** | Your Anthropic key (password-masked) |
| **Sub-questions** | Slider 3–6: more = richer report, slower |
| **Model** | Sonnet (recommended) or Haiku (faster/cheaper) |

---

## 📊 Example Topics to Try

| Topic | What you'll get |
|-------|----------------|
| "The impact of quantum computing on cybersecurity" | Technical depth + practical implications |
| "History and future of renewable energy" | Timeline + policy + technology |
| "How large language models are trained" | Architecture, data, RLHF explained |
| "Effects of sleep deprivation on cognitive performance" | Neuroscience + practical health insights |
| "Rise of electric vehicles in India" | Market, infrastructure, policy, challenges |

---

## 🧩 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│  ┌──────────────┐   ┌────────────────┐  ┌───────────┐  │
│  │  Text Input  │   │  Progress Bar  │  │  Report   │  │
│  │  (topic)     │   │  + QA Cards    │  │  + DL btn │  │
│  └──────┬───────┘   └───────▲────────┘  └─────▲─────┘  │
│         │                   │                  │         │
└─────────┼───────────────────┼──────────────────┼─────────┘
          │                   │                  │
          ▼                   │                  │
    ┌─────────────────────────────────────────────────┐
    │              Python Agent Logic                  │
    │  plan_sub_questions() → [q1, q2, q3, q4]        │
    │  for each q: research_sub_question()  ──────────►│
    │  generate_final_report(all answers)             │
    └──────────────────────┬──────────────────────────┘
                           │  HTTPS API calls
                           ▼
              ┌─────────────────────────┐
              │   Anthropic Claude API   │
              │   /v1/messages endpoint  │
              └─────────────────────────┘
```

---

## 🔧 Customisation Ideas

- **Add real web search**: Integrate `serpapi` or `duckduckgo-search` to fetch live URLs before answering each sub-question
- **Export to PDF**: Use `fpdf2` or `reportlab` to convert the Markdown report to PDF
- **Memory across sessions**: Store past reports in `sqlite3` or a JSON file
- **Multi-language support**: Add a language selector and append "Respond in [language]" to the system prompt
- **Streaming output**: Use `client.messages.stream()` for word-by-word output

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `AuthenticationError` | Check your API key — make sure it starts with `sk-ant-` |
| `RateLimitError` | Wait 30 seconds, or reduce the number of sub-questions |
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit anthropic` |
| App opens but blank | Hard-refresh the browser (Ctrl+Shift+R) |
| Port already in use | Run `streamlit run app.py --server.port 8502` |

---

## 📄 License

MIT — free to use, modify, and share.