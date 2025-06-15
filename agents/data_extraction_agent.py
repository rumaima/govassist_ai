# data_extraction_agent.py
import os
import fitz  # PyMuPDF
import pandas as pd

class DataExtractionAgent:
    def __init__(self):
        pass

    def extract_text_from_txt(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"❌ Error reading TXT file: {e}")

    def extract_data_from_excel(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        try:
            df = pd.read_excel(path)
            return df.to_dict(orient="records")
        except Exception as e:
            raise ValueError(f"❌ Error reading Excel: {e}")

    def route_files(self, file_paths):
        file_dict = {}
        for path in file_paths:
            fname = os.path.basename(path).lower()
            if "emirates" in fname:
                file_dict["emirates_id"] = path
            elif "bank" in fname:
                file_dict["bank_statement"] = path
            elif "resume" in fname:
                file_dict["resume"] = path
            elif "credit" in fname:
                file_dict["credit_report"] = path
            elif "asset" in fname or "liability" in fname:
                file_dict["assets_and_liabilities"] = path
        return file_dict

    def extract(self, file_paths):
        file_dict = self.route_files(file_paths)

        required = ["emirates_id", "bank_statement", "resume", "credit_report", "assets_and_liabilities"]
        missing = [f for f in required if f not in file_dict]
        if missing:
            raise ValueError(f"⚠️ Missing required files: {', '.join(missing)}")

        output = {}
        output["emirates_id_text"] = self.extract_text_from_txt(file_dict["emirates_id"])
        output["bank_statement_text"] = self.extract_text_from_txt(file_dict["bank_statement"])
        output["resume_text"] = self.extract_text_from_txt(file_dict["resume"])
        output["credit_report_text"] = self.extract_text_from_txt(file_dict["credit_report"])
        output["assets_info"] = self.extract_data_from_excel(file_dict["assets_and_liabilities"])

        return output