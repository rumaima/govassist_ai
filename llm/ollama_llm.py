import os
from langchain_community.llms import Ollama
from langchain_core.exceptions import OutputParserException

# Get the base URL from environment or default to Docker service hostname
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
# Choose your model here
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Initialize the model
ollama_model = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

def query_llama(prompt: str) -> str:
    try:
        response = ollama_model.invoke(prompt)
        print(response)
        return str(response)
    except Exception as e:
        return f"❌ Error during LLM inference: {e}"