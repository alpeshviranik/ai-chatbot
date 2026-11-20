# 🩺 Diabetes Patient Query Chatbot

An AI chatbot that answers patient questions about diabetes using a **retrieval-augmented generation (RAG)** pipeline, with built-in **safety guardrails** that escalate emergencies and refuse medication-dosing advice.

> ⚠️ **Medical disclaimer:** This project is a technical demonstration and educational tool. It is **not** a medical device and does **not** provide medical advice, diagnosis, or treatment. The sample knowledge base is illustrative only. Any real deployment must use clinician-reviewed content and go through appropriate clinical, legal, and regulatory review (e.g., HIPAA/GDPR, local medical-device rules).

---

## ✨ Features

- **Grounded answers**: retrieves relevant passages from a curated knowledge base and answers only from them.
- **Safety layer (runs before the LLM)**: detects emergencies (severe hypoglycemia, DKA symptoms, self-harm, chest pain) and returns an immediate "seek emergency care" message.
- **Dosing guardrail**: requests to change insulin or medication doses are redirected to the patient's care team.
- **Source citations**: every answer lists the knowledge-base sections it used.
- **Multi-turn memory** per session.
- **Interfaces**: REST API (FastAPI) and a command-line chat.
- **Tests + CI** with GitHub Actions.

## 🏗️ Architecture

```
Patient message
      │
      ▼
┌───────────────┐  emergency / self-harm  ┌──────────────────────┐
│ Safety check  │ ───────────────────────▶│ Fixed escalation msg │
└──────┬────────┘                         └──────────────────────┘
       │ ok / dosing
       ▼
┌───────────────┐   top-k passages   ┌─────────────┐
│ TF-IDF        │ ─────────────────▶ │ Claude LLM  │ ──▶ Answer + sources
│ retriever     │                    │ (grounded)  │
└───────────────┘                    └─────────────┘
```

## 📁 Project structure

```
diabetes-chatbot/
├── data/knowledge/          # Markdown knowledge base (replace with vetted content)
├── src/diabetes_bot/
│   ├── config.py            # Settings via environment variables
│   ├── safety.py            # Emergency + dosing detection
│   ├── retriever.py         # TF-IDF retrieval over markdown sections
│   ├── chatbot.py           # Orchestration + LLM call
│   ├── api.py               # FastAPI app
│   └── cli.py               # Terminal chat
├── tests/
├── requirements.txt
└── .env.example
```

## 🚀 Quick start

```bash
git clone https://github.com/<your-username>/diabetes-chatbot.git
cd diabetes-chatbot

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # then add your ANTHROPIC_API_KEY
```

### Chat in the terminal
```bash
python -m diabetes_bot.cli
```

### Run the API
```bash
uvicorn diabetes_bot.api:app --reload
```

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo", "message": "What should I do if my sugar is 60?"}'
```

Response:
```json
{
  "answer": "...",
  "sources": ["Hypoglycemia > The 15-15 rule"],
  "escalated": false
}
```

Interactive docs: http://localhost:8000/docs

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Your API key (required) |
| `MODEL_NAME` | `claude-sonnet-5-5` | Claude model to use |
| `TOP_K` | `3` | Passages retrieved per question |
| `MAX_HISTORY_TURNS` | `6` | Conversation turns remembered |
| `KNOWLEDGE_DIR` | `data/knowledge` | Folder of `.md` files |

## 📚 Adding your own knowledge

Drop `.md` files into `data/knowledge/`. Use `# Title` for the topic and `## Section` headings. Each section becomes one retrievable passage. Content should come from trusted, clinician-reviewed sources (e.g., ADA, NIDDK, local guidelines).

## 🧪 Tests

```bash
pip install pytest
PYTHONPATH=src pytest -q
```

## 🛡️ Safety design

1. **Rule-based triage runs first**, so emergencies never depend on LLM behavior.
2. The system prompt forbids diagnosis, dosing changes, and answers outside the retrieved context.
3. If retrieval finds nothing relevant, the bot says it doesn't know and suggests contacting a clinician.
4. No PHI is logged by default. Do not add logging of patient messages without proper consent and safeguards.

## 🗺️ Roadmap

- [ ] Semantic embeddings + vector DB (replace TF-IDF)
- [ ] Multilingual support
- [ ] Web chat UI
- [ ] Carb counting / glucose log integration
- [ ] Clinician handoff and audit trail
- [ ] Evaluation set with clinician-graded answers

## 🤝 Contributing

Issues and PRs are welcome. Medical content contributions must cite a reputable source.

## 📄 License

MIT. See [LICENSE](LICENSE).
