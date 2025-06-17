import os
from models.invoice_data import InvoiceData
from services.template_service import TemplateService
from services.pdf_service import PDFService
import os

# template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
# print(f"📄 Using template: {template_path}")

def generate_invoice_pdf():
    print("Generating invoice PDF...")
    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
    output_dir = "output"
    output_filename = "invoice_001"
    
    filled_docx_path = os.path.join(output_dir, f"{output_filename}.docx")

    # Data input
    data = InvoiceData(
        name="Nandha Kumar",
        date="2025-06-16",
        amount="₹15,000",
        invoice_id="INV-20250616-001"
    )

    # # Step 1: Fill Word template
    template_service = TemplateService(template_path)
    template_service.fill_template(filled_docx_path, data.to_dict())

    # # Step 2: Convert to PDF
    # pdf_service = PDFService(output_dir)
    # pdf_path = pdf_service.convert_to_pdf(filled_docx_path, output_filename)

    # print(f"✅ PDF generated at: {pdf_path}")

if __name__ == "__main__":
    generate_invoice_pdf()
