import os
from docx2pdf import convert
from datetime import datetime
from utils.dates import generate_dir_name
output_dir = os.getenv("OUTPUT_DIR") or "output"


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
        
        # Normalize path for cross-platform compatibility (use forward slashes)
        normalized_path = path.replace(os.sep, '/')
        return normalized_path
