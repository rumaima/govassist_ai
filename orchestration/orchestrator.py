from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver
from langchain_core.runnables import RunnableLambda
from agents.data_extraction_agent import DataExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.eligibility_agent import EligibilityAgent
from agents.enablement_agent import EnablementAgent

def extract_node(state):
    extractor = DataExtractionAgent()
    result = extractor.process_application(state['file_dict'])
    return {"extracted_data": result}

def validate_node(state):
    validator = ValidationAgent()
    result = validator.run_validation(state["extracted_data"])
    return {"validation_result": result}

def eligibility_node(state):
    eligibility = EligibilityAgent()
    result = eligibility.predict(state["extracted_data"])
    return {"eligibility_result": result}

def enablement_node(state):
    enablement = EnablementAgent()
    result = enablement.recommend(state["extracted_data"].get("resume_text", ""))
    return {"recommendations": result}

def check_validation_result(state):
    return "valid" if state["validation_result"]["valid"] else "invalid"

def build_graph():
    builder = StateGraph()
    builder.add_node("Extract", RunnableLambda(extract_node))
    builder.add_node("Validate", RunnableLambda(validate_node))
    builder.add_node("Eligibility", RunnableLambda(eligibility_node))
    builder.add_node("Enablement", RunnableLambda(enablement_node))

    builder.set_entry_point("Extract")
    builder.add_edge("Extract", "Validate")
    builder.add_conditional_edges("Validate", check_validation_result, {
        "valid": "Eligibility",
        "invalid": "end"
    })
    builder.add_edge("Eligibility", "Enablement")
    builder.add_edge("Enablement", "end")

    return builder.compile()