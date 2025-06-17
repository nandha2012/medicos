import os
from docx2pdf import convert

class PDFService:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_to_pdf(self, docx_path: str, output_filename: str):
        output_pdf_path = os.path.join(self.output_dir, f"{output_filename}.pdf")
        convert(docx_path, output_pdf_path)
        return output_pdf_path
