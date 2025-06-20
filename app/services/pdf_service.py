import os
from docx2pdf import convert
from datetime import datetime
output_dir = os.getenv("OUTPUT_DIR") or "output"
def generate_dir_name():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")

class PDFService:
    
    def __init__(self):
        self.output_dir = output_dir+"/"+generate_dir_name()
        print(f"output_dir {self.output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_to_pdf(self, docx_path: str,output_path, output_filename: str):
        file_path = self.output_dir+"/"+output_path
        path = os.path.join(file_path, f"{output_filename}.pdf")
        print(f"📄 Output PDF path: {path}")
        convert(docx_path, path)
        return path
