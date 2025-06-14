import requests

SYSTEM_PROMPT = """You are GovAssistBot, a helpful assistant for a government financial support system.
Answer questions about eligibility, application status, document requirements, or appeal options.
If user was soft-declined, suggest helpful next steps (e.g., training, resume update, asset clarification)."""

FEW_SHOT_CONTEXT = """
Q: Why was my application declined?
A: Based on our validation and eligibility checks, your income may be above the threshold or your documents were inconsistent.

Q: What documents should I upload?
A: Please upload Emirates ID, resume, bank statement, asset/liability file (Excel), and credit report.

Q: Can I appeal the decision?
A: Yes, you can submit new documents or clarification. If your employment status changed, please upload an updated resume.
"""

def ask_chatbot(user_query):
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": FEW_SHOT_CONTEXT},
            {"role": "user", "content": user_query}
        ],
        "stream": False
    }
    try:
        res = requests.post("http://localhost:11434/api/chat", json=payload)
        return res.json()['message']['content']
    except Exception as e:
        return f"⚠️ Chat failed: {str(e)}"