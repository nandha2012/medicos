import os
from docx2pdf import convert
from datetime import datetime

def generate_dir_name():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")

class PDFService:
    
    def __init__(self):
        self.output_dir = "output"+"/"+generate_dir_name()
        print(f"output_dir {self.output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_to_pdf(self, docx_path: str,file_path, output_filename: str):
        output_pdf_path = os.path.join(file_path, f"{output_filename}.pdf")
        convert(docx_path, output_pdf_path)
        return output_pdf_path
