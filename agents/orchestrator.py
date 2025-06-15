import os
from typing import TypedDict, List, Dict, Any

from agents.data_extraction_agent import DataExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.eligibility_agent import EligibilityAgent
from agents.enablement_agent import EnablementAgent
from llm.ollama_llm import query_llama  # <-- Add this import

from langgraph.graph import StateGraph
from langsmith.run_helpers import traceable as langsmith_traceable

# Set LangSmith project settings
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "GovAssistPipeline"

# Define state schema
class PipelineState(TypedDict, total=False):
    form_inputs: Dict[str, Any]
    file_paths: List[str]
    extracted_data: Dict[str, Any]
    validation_result: Dict[str, Any]
    eligibility_result: Dict[str, Any]
    enablement_result: List[Dict[str, Any]]
    llm_reasoning: str

# Load agents
extractor = DataExtractionAgent()
validator = ValidationAgent()
eligibility = EligibilityAgent()
enablement = EnablementAgent()

@langsmith_traceable(name="DataExtraction")
def extract_step(state: PipelineState) -> PipelineState:
    file_paths = state.get("file_paths", [])
    print("File paths within orchestrator:extract_step()")
    print(file_paths)
    extracted = extractor.extract(file_paths)
    return {**state, "extracted_data": extracted}

@langsmith_traceable(name="MergeFormInputs")
def merge_form_step(state: PipelineState) -> PipelineState:
    form_inputs = state.get("form_inputs", {})
    enriched = state.get("extracted_data", {})

    enriched.update({
        "full_name": form_inputs.get("name"),
        "user_income": float(form_inputs.get("income", 0)),
        "family_size": int(form_inputs.get("family_size", 1)),
        "age": int(form_inputs.get("age", 0)),
        "manual_employment_status": form_inputs.get("employment_status", "")
    })

    return {**state, "extracted_data": enriched}

@langsmith_traceable(name="Validation")
def validate_step(state: PipelineState) -> PipelineState:
    result = validator.run_validation(state["extracted_data"])
    return {**state, "validation_result": result}

@langsmith_traceable(name="LLM Reasoning")
def llama_reasoning_step(state: PipelineState) -> PipelineState:
    prompt = f"""
    You are a government support assistant reviewing the following data:

    Extracted Data:
    {state.get("extracted_data")}

    Provide a helpful summary or flag any missing or conflicting information.
    """
    print("🧠 LLM Prompt:\n", prompt)

    response = query_llama(prompt)
    print("🧠 LLM Response:\n", response)  # <-- Add this line

    return {**state, "llm_reasoning": response}

@langsmith_traceable(name="EligibilityCheck")
def eligibility_step(state: PipelineState) -> PipelineState:
    result = eligibility.predict(state["extracted_data"])
    return {**state, "eligibility_result": result}

@langsmith_traceable(name="EnablementSupport")
def enablement_step(state: PipelineState) -> PipelineState:
    resume_text = state["extracted_data"].get("resume_text", "")
    if not resume_text.strip():
        return {**state, "enablement_result": []}
    matches = enablement.recommend(resume_text)
    return {**state, "enablement_result": matches}

@langsmith_traceable(name="AggregateOutput")
def format_result(state: PipelineState) -> Dict[str, Any]:
    print("🧾 Aggregating Final Output. State:\n", state)  # Add this line
    eligibility_res = state["eligibility_result"]
    enablement_res = state.get("enablement_result", [])

    support = []
    if eligibility_res["eligible"]:
        support.append("Financial Aid")
    else:
        if enablement_res:
            support.extend([f"Upskill: {r['job_title']}" for r in enablement_res])
        else:
            support.append("Referral to Career Counseling")

    return {
        "status": "Approved" if eligibility_res["eligible"] else "Soft Decline",
        "eligibility_score": int(eligibility_res["confidence"] * 100),
        "recommended_support": support,
        "validation": state.get("validation_result"),
        "llm_notes": state.get("llm_reasoning"),
        "input_summary": {
            "files_received": state.get("file_paths", []),
            "form": state.get("form_inputs", {})
        }
    }

# ✅ Build LangGraph using state_schema
graph = StateGraph(state_schema=PipelineState)

graph.add_node("extract", extract_step)
graph.add_node("merge_form", merge_form_step)
graph.add_node("validate", validate_step)
graph.add_node("llama_reasoning", llama_reasoning_step)
graph.add_node("check_eligibility", eligibility_step)
graph.add_node("enablement", enablement_step)
graph.add_node("aggregate", format_result)

graph.set_entry_point("extract")
graph.add_edge("extract", "merge_form")
graph.add_edge("merge_form", "validate")
graph.add_edge("validate", "llama_reasoning")
graph.add_edge("llama_reasoning", "check_eligibility")
graph.add_edge("check_eligibility", "enablement")
graph.add_edge("enablement", "aggregate")

runnable_graph = graph.compile()

# Public API
def run_decision_pipeline(form_inputs, file_paths):
    initial_state = {
        "form_inputs": form_inputs,
        "file_paths": file_paths
    }
    return runnable_graph.invoke(initial_state)
