# GovAssist AI 💼🤖

GovAssist AI is an end-to-end AI-powered automation system built for government social support departments. It processes applications in minutes using locally hosted multimodal agents, large language models (LLMs), and agentic orchestration. Designed for scalability, explainability, and fairness.

---

## 🚀 Features

- ✅ Fully automated decision-making pipeline (extract → validate → decide)
- 📄 Multimodal document ingestion (PDFs, images, Excel)
- 🧠 ML-based eligibility classification (Random Forest)
- 💬 Chatbot assistant powered by local LLM (Ollama)
- 📝 Appeal and feedback submission system
- 📊 Admin dashboard for audit and analytics
- 🔗 LangGraph-based agent orchestration
- 🧾 PostgreSQL for decisions + appeals tracking

---

## 📂 Folder Structure

```
govassist_ai/
├── agents/             # Core agents: extraction, validation, eligibility, enablement
├── chat/               # LLM-powered chatbot assistant
├── frontend/           # Gradio user interface and appeal/dashboard modules
├── models/             # Training script and ML model
├── orchestration/      # LangGraph-based pipeline orchestrator
├── samples/            # Sample documents for testing
├── storage/            # PostgreSQL table schema
├── main_test_pipeline.py   # CLI pipeline runner (no UI)
├── requirements.txt    # Python dependencies
├── config.yaml         # App config template
└── README.md           # This file
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/govassist_ai.git
cd govassist_ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

```sql
-- Run this in your PostgreSQL shell
CREATE DATABASE govassist;

-- Then execute:
psql -d govassist -f storage/postgres_config.sql
```

### 5. Pull a local LLM using Ollama

```bash
# Install Ollama: https://ollama.com/download
ollama pull mistral
```

---

## 🧪 Run the Full System

```bash
python frontend/frontend_app.py
```

Visit `http://localhost:7860` to use:
- 📤 Application Upload
- 💬 Chatbot Assistant
- 📝 Appeal Submission
- 📊 Admin Dashboard

---

## 🧠 Orchestration Engine

We use **LangGraph** to orchestrate agents:
- `DataExtractionAgent`
- `ValidationAgent`
- `EligibilityAgent`
- `EnablementAgent`

You can run the orchestrator standalone with:

```bash
python orchestration/orchestrator.py
```

---

## 📊 Admin Dashboard

- Visual insights from applications
- Filter decisions, top job matches
- View appeal text + re-evaluation requests

---

## 🔐 LLM Hosting Locally

We use [Ollama](https://ollama.com/) to run models like Mistral or LLaMA3 locally:
- Private
- Fast inference
- No internet needed

---

## 🛠️ Tools & Stack

| Layer              | Tools Used                                    |
|--------------------|-----------------------------------------------|
| UI                 | Gradio                                        |
| Agent Orchestration| LangGraph, LangChain                          |
| ML Models          | scikit-learn (RandomForest)                  |
| Embeddings + Search| SentenceTransformers + ChromaDB              |
| LLM                | Mistral via Ollama                            |
| Storage            | PostgreSQL                                    |

---

## 📌 Author & Credits

Developed by: **Your Name**  
For demo purposes in government enablement + AI automation systems.

---

## 📃 License

MIT License. Use responsibly.