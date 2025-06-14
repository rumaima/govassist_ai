import os
import fitz  # PyMuPDF
import pandas as pd
import easyocr
import re

class DataExtractionAgent:
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['en'])

    def extract_from_emirates_id(self, image_path):
        result = self.ocr_reader.readtext(image_path, detail=0)
        ocr_text = " ".join(result)
        return {
            "full_name": self.extract_name(ocr_text),
            "id_number": self.extract_id(ocr_text)
        }

    def extract_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = " ".join([page.get_text() for page in doc])
        return text

    def extract_from_excel(self, excel_path):
        df = pd.read_excel(excel_path)
        return df.to_dict(orient='records')

    def extract_income(self, text):
        matches = re.findall(r"(?:AED|Dirhams|Dhs)?\s?(\d{4,6})", text)
        return max(map(int, matches)) if matches else None

    def extract_name(self, text):
        match = re.search(r"Name[:\-]?\s*([A-Z][a-z]+\s[A-Z][a-z]+)", text)
        return match.group(1) if match else "Unknown"

    def extract_id(self, text):
        match = re.search(r"\b784-\d{4}-\d{7}-\d\b", text)
        return match.group(0) if match else "Unknown"

    def process_application(self, file_dict):
        output = {}

        if 'emirates_id' in file_dict:
            output['emirates_id_info'] = self.extract_from_emirates_id(file_dict['emirates_id'])

        if 'resume' in file_dict:
            resume_text = self.extract_from_pdf(file_dict['resume'])
            output['resume_text'] = resume_text
            output['extracted_name'] = self.extract_name(resume_text)

        if 'bank_statement' in file_dict:
            bank_text = self.extract_from_pdf(file_dict['bank_statement'])
            output['estimated_income'] = self.extract_income(bank_text)

        if 'assets_file' in file_dict:
            output['assets_info'] = self.extract_from_excel(file_dict['assets_file'])

        if 'credit_report' in file_dict:
            credit_text = self.extract_from_pdf(file_dict['credit_report'])
            output['credit_income'] = self.extract_income(credit_text)

        return output