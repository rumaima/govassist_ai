
# GovAssist AI: Automated Social Support Eligibility System

GovAssist AI is an intelligent assistant for government social support programs. It takes user-provided information (forms and documents) and uses LLMs and rule-based logic to extract data, validate it, assess eligibility, and recommend next steps.

---

## 📁 File Descriptions

### `frontend_app.py`
Gradio-based web UI for uploading files and entering applicant details. Displays results and interacts with the `orchestrator`.

### `orchestrator.py`
Main controller coordinating the decision pipeline. Calls each agent in order:
- `DataExtractionAgent`
- `ValidationAgent`
- `EligibilityAgent`
- `EnablementAgent`
And uses LLM via `ollama_llm.py` for reasoning.

### `ollama_llm.py`
Contains the wrapper for interacting with the Ollama LLM. Takes extracted data and prompts the model to provide insights and summary reasoning.

### `data_extraction_agent.py`
Extracts structured information from raw text/Excel files (emirates ID, bank statement, resume, credit report, and asset info).

### `validation_agent.py`
Validates input format and flags missing/inconsistent fields (e.g., invalid ID, mismatched income values).

### `eligibility_agent.py`
Loads and uses a pretrained classifier to determine whether the applicant qualifies for social support.

### `eligibility_model_trainer.py`
Optional training script for fitting a scikit-learn classifier for eligibility determination (Random Forest, etc.).

### `enablement_agent.py`
Suggests possible job titles or government programs based on resume content using a rule-based relevance match.

---

## 🐳 Running via Docker

### 1. Clone and Enter Project Folder

```bash
git clone https://github.com/your-org/govassist_ai.git
cd govassist_ai
```

### 2. Build and Run Container

```bash
docker build -t govassist_cuda .
docker run -dit --gpus all --network ollama-net -e OLLAMA_URL=http://ollama:11434 -e OLLAMA_MODEL=llama3 -p 7860:7860 --name govassist_app govassist_cuda
docker logs -f govassist_app
```

Make sure `ollama` is installed and running on your host machine:
```bash
ollama run llama3
```

---

## ✅ Example Usage

Go to `http://localhost:7860` and:
1. Fill in the applicant details.
2. Upload required documents (.txt and .xlsx).
3. Click on the button Submit for Evaluation to get automated analysis, validation issues, eligibility result, and support suggestions.

---

## 📌 Notes

- Compatible with local Ollama LLM inference.
- Can be extended with LangGraph + LangSmith tracing.
- Designed for modularity — swap agents or models as needed.
- Samples of two users present under the folder 'samples_user_docs'

---
