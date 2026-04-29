# 🔬 Smart Research Agent

> An AI-powered multi-step research agent that **plans**, **researches**, and **reports** — automatically.
> Built with Python, Streamlit, and HuggingFace (Qwen2.5-72B) — completely free to use!

---

## 🚀 Live Demo

🔗 **[Click here to try the app](https://smart-research-agent.streamlit.app/)**

---

## 📦 Project Structure

```
smart-research-agent/
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python packages list
└── README.md         ← This file
```

---

## ⚙️ How It Works

The agent follows a 3-step workflow:

```
User types a topic
        ↓
STEP 1 — PLAN      Break topic into 4 sub-questions
        ↓
STEP 2 — RESEARCH  Answer each sub-question using AI
        ↓
STEP 3 — REPORT    Write a full structured report
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core programming language |
| Streamlit | Web app UI framework |
| HuggingFace API | Free AI model access |
| Qwen2.5-72B | LLM for research & writing |

---

## 💻 Run Locally

### Step 1 — Install packages
```bash
pip install streamlit huggingface_hub
```

### Step 2 — Run the app
```bash
streamlit run app.py
```

### Step 3 — Open browser
```
http://localhost:8501
```

### Step 4 — Get Free API Key
1. Go to → **https://huggingface.co/settings/tokens**
2. Click **"New token"** → Role: **Read**
3. Copy token (`hf_...`) → paste in sidebar

---

## 🔑 API Key Setup (Free)

**No credit card needed!** HuggingFace tokens are completely free.

### For Local Use:
Paste your `hf_...` token in the sidebar when running locally.

### For Deployed App (Streamlit Cloud):
Add this in Streamlit Cloud → Advanced Settings → Secrets:
```
HF_API_KEY = "hf_your_token_here"
```

---

## 📊 Example Topics to Try

| Topic | Output |
|-------|--------|
| Impact of AI on jobs | Career trends + future predictions |
| Future of electric vehicles in India | Market + infrastructure + policy |
| How does machine learning work | Concepts + algorithms explained |
| Effects of social media on students | Research + mental health insights |
| Climate change solutions 2025 | Technology + policy + innovation |

---

## 🧩 Agent Architecture

```
┌─────────────────────────────────────┐
│         Streamlit Frontend          │
│  Topic Input → Progress → Report    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Python Agent Logic          │
│                                     │
│  1. plan_sub_questions()            │
│     → ["Q1", "Q2", "Q3", "Q4"]     │
│                                     │
│  2. research_sub_question() x 4     │
│     → answers for each question     │
│                                     │
│  3. generate_final_report()         │
│     → structured markdown report    │
└──────────────┬──────────────────────┘
               │ API calls
               ▼
┌─────────────────────────────────────┐
│    HuggingFace Inference API        │
│    Model: Qwen2.5-72B-Instruct      │
│    Cost: FREE                       │
└─────────────────────────────────────┘
```

---

## 🚀 Deploy on Streamlit Cloud (Free)

1. Push code to GitHub (public repo)
2. Go to → **https://share.streamlit.io**
3. Click **"Create app"**
4. Select your repo → file: `app.py`
5. Click **"Advanced settings"** → Secrets:
   ```
   HF_API_KEY = "hf_your_token_here"
   ```
6. Click **"Deploy!"** → get your live link

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `401 Unauthorized` | Wrong HF token — regenerate at huggingface.co/settings/tokens |
| `404 Not Found` | Model unavailable — already fixed, using Qwen2.5-72B |
| `Model is loading` | Wait 30 seconds — free tier cold start |
| `ModuleNotFoundError` | Run `pip install streamlit huggingface_hub` |
| App blank on open | Hard refresh browser (Ctrl + Shift + R) |
| Port already in use | Run `streamlit run app.py --server.port 8502` |

---

## Features

- Fully automatic research pipeline
- AI breaks any topic into smart sub-questions
- Each sub-question answered in detail
- Final structured report with summary + conclusion
- Download report as .md file
- Clean modern UI
- 100% free — no paid API needed

---

## Author

**Aarzoo** — AI & Python Developer
Built as part of an AI-based agentic automation project.

---

## 📄 License

MIT — free to use, modify, and share.
