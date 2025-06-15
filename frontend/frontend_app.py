
import gradio as gr
import os
import sys
import shutil
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.orchestrator import run_decision_pipeline

# Backend inference using real orchestrator
def run_inference(file_inputs, form_inputs):
    try:
        print("📥 Received form inputs:", form_inputs)
        print("📎 Received file objects:", file_inputs)

        file_paths = []
        os.makedirs("temp_uploads", exist_ok=True)

        for idx, fpath in enumerate(file_inputs):
            if fpath is not None:
                fname = os.path.basename(fpath)
                dest_path = os.path.join("temp_uploads", fname)
                shutil.copy(fpath, dest_path)
                file_paths.append(dest_path)

        print("✅ Final list of file paths:", file_paths)

        try:
            result = run_decision_pipeline(form_inputs, file_paths)
            print("🎯 Result from pipeline:", result)
            return result
        except Exception as pipeline_error:
            print("🔥 Pipeline error:")
            traceback.print_exc()
            return {"error": str(pipeline_error)}

    except Exception as e:
        print("🔥 Exception occurred outside pipeline:")
        traceback.print_exc()
        return {"error": str(e)}

def format_output(result):
    if "error" in result:
        return f"❌ Error: {result['error']}"

    file_names = [os.path.basename(f) for f in result.get('file_paths', [])]
    llm_summary = result.get('llm_reasoning', 'No summary provided.')

    form_inputs = result.get('form_inputs', {})
    eligibility_result = result.get('eligibility_result', {})
    enablement_result = result.get('enablement_result', [])

    lines = [
        f"📝 **Applicant Info:** " + " ".join([f"**{k.capitalize()}**: {v}" for k, v in form_inputs.items()]),
        f"✅ **Eligibility:** {'Eligible' if eligibility_result.get('eligible') else 'Not Eligible'}",
        f"📊 **Confidence Score:** {eligibility_result.get('confidence', 0.0) * 100:.2f}%",
        f"🎯 **Recommended Jobs:** - " + " - ".join([f"{j['job_title']} (Relevance: {j['relevance']:.2f})" for j in enablement_result]),
        f"📂 **Files Received:** - " + " - ".join(file_names),
        f"🧠 **LLM Summary Notes:** {llm_summary}",
    ]
    return "\n\n".join(lines)

def app_interface(*inputs):
    file_inputs = inputs[5:]
    print("File Inputs within frontend_app.py:app_interface()")
    print(file_inputs)
    form_inputs = {
        "name": inputs[0],
        "income": inputs[1],
        "employment_status": inputs[2],
        "family_size": inputs[3],
        "age": inputs[4]
    }
    print("Form Inputs within frontend_app.py:app_interface()")
    print(form_inputs)
    try:
        result = run_inference(file_inputs, form_inputs)
        print(result)
        return format_output(result)
    except Exception as e:
        return format_output({"error": str(e)})

form_inputs = [
    gr.Textbox(label="👤 Applicant Name", placeholder="Enter full name"),
    gr.Textbox(label="💰 Monthly Income (AED)", placeholder="e.g. 12000"),
    gr.Textbox(label="💼 Employment Status", placeholder="Employed, Unemployed, Freelance"),
    gr.Textbox(label="👥 Family Size", placeholder="e.g. 4"),
    gr.Textbox(label="👱️ Age", placeholder="e.g. 35")
]

file_inputs = [
    gr.File(label="📎 Upload Emirates ID (TXT)", file_types=[".txt"], interactive=True),
    gr.File(label="📎 Upload Bank Statement (TXT)", file_types=[".txt"], interactive=True),
    gr.File(label="📎 Upload Resume (TXT)", file_types=[".txt"], interactive=True),
    gr.File(label="📎 Upload Assets and Liabilities (Excel)", file_types=[".xlsx"], interactive=True),
    gr.File(label="📎 Upload Credit Report (TXT)", file_types=[".txt"], interactive=True)
]

with gr.Blocks(title="GovAssist AI") as iface:
    gr.Markdown("""
    # 🌟 Gov AI Social Support Eligibility System
    Welcome to the automated application assistant. Please complete the form and upload the necessary documents to begin your eligibility check.
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📋 Application Form")
            for f in form_inputs:
                f.render()

        with gr.Column():
            gr.Markdown("### 📂 Upload Documents")
            for f in file_inputs:
                f.render()

    submit_btn = gr.Button("✅ Submit for Evaluation")
    output = gr.Markdown(label="📊 Assessment Result")
    flag_btn = gr.Button("🚩 Flag / Report This Result")

    submit_btn.click(fn=app_interface, inputs=form_inputs + file_inputs, outputs=output)
    flag_btn.click(fn=lambda: "⚠️ Thank you. The result has been flagged for review.", inputs=[], outputs=output)

if __name__ == '__main__':
    iface.launch(server_name="0.0.0.0", server_port=7860, debug=True)
