import re

class ValidationAgent:
    def __init__(self, income_tolerance_percent=15):
        self.income_tolerance = income_tolerance_percent

    def validate_name_match(self, id_name, resume_name):
        if id_name.lower() == resume_name.lower():
            return True, ""
        return False, f"Name mismatch: ID says '{id_name}', Resume says '{resume_name}'"

    def validate_id_format(self, id_number):
        if re.match(r"784-\d{4}-\d{7}-\d", id_number):
            return True, ""
        return False, f"Invalid Emirates ID format: {id_number}"

    def validate_income_range(self, income1, income2):
        if not income1 or not income2:
            return False, "Missing income data from either bank or credit report"
        diff_percent = abs(income1 - income2) / max(income1, income2) * 100
        if diff_percent > self.income_tolerance:
            return False, f"Income mismatch: AED {income1} vs AED {income2} (>{self.income_tolerance}% deviation)"
        return True, ""

    def validate_resume(self, resume_text):
        if len(resume_text.strip()) >= 100:
            return True, ""
        return False, "Resume text is too short or empty."

    def validate_assets(self, assets_list):
        for asset in assets_list:
            if 'Asset Type' not in asset or 'Value' not in asset:
                return False, "Missing asset fields in submitted asset document"
        return True, ""

    def run_validation(self, extracted_data):
        report = {
            "valid": True,
            "issues": []
        }

        name_check, msg = self.validate_name_match(
            extracted_data.get('emirates_id_info', {}).get('full_name', ""),
            extracted_data.get('extracted_name', "")
        )
        if not name_check:
            report["valid"] = False
            report["issues"].append(msg)

        id_check, msg = self.validate_id_format(
            extracted_data.get('emirates_id_info', {}).get('id_number', "")
        )
        if not id_check:
            report["valid"] = False
            report["issues"].append(msg)

        income_check, msg = self.validate_income_range(
            extracted_data.get('estimated_income'),
            extracted_data.get('credit_income')
        )
        if not income_check:
            report["valid"] = False
            report["issues"].append(msg)

        resume_check, msg = self.validate_resume(
            extracted_data.get('resume_text', "")
        )
        if not resume_check:
            report["valid"] = False
            report["issues"].append(msg)

        if 'assets_info' in extracted_data:
            assets_check, msg = self.validate_assets(extracted_data['assets_info'])
            if not assets_check:
                report["valid"] = False
                report["issues"].append(msg)

        return report