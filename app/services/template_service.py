from docx import Document
import os

class TemplateService:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def fill_template(self, output_path: str, data: dict):
        print(f"📄 Using template: {self.template_path}")
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"❌ Template not found at: {self.template_path}")
        doc = Document(self.template_path)  

        for para in doc.paragraphs:
            for key, value in data.items():
                if f"{{{{{key}}}}}" in para.text:
                    para.text = para.text.replace(f"{{{{{key}}}}}", str(value))

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in data.items():
                        if f"{{{{{key}}}}}" in cell.text:
                            cell.text = cell.text.replace(f"{{{{{key}}}}}", str(value))

        doc.save(output_path)