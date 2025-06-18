import os
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from services.template_service import TemplateService
from services.pdf_service import PDFService
import os

# template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
# print(f"📄 Using template: {template_path}")

def generate_invoice_pdf():
    print("Generating invoice PDF...")
    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)


    # Data input
    data = RedcapResponseFirst(
        timestamp="2025-06-17 09:06",
        username="dc49dqm",
        action="Update record TNSC022038654",
        details="",
        record="TNSC022038654"
    )



    data2 = RedcapResponseSecond(
        mg_idpreg="dfsfsdf",
        DELIVERY_DATE="2022-01-04",
        redcap_repeat_instrument="",
        redcap_repeat_instance="",
        ifu_fac_phone="",
        ifu_fac_num="",
        bc_momnamefirst="SHELBY",
        bc_momnamelast="ROBINSON",
        bc_momssn="412810789",
        inf_dob_mom_tr="2022-01-04",
        hos_name_cat_2="9",
        bc_mom_dob="2022-01-04",
        mr_request_dt="2024-11-04",
        hospital_fax_num="615-523-1525",
        hospital_phone_num="615-523-1525",
        mr_rec_needs___1="1",
        mr_rec_needs___2="0",
        mr_rec_needs___3="0",
        mr_rec_needs___4="0",
        mr_rec_needs___6="0",
        mr_rec_needs___7="0",
        mr_rec_needs___8="0",
        mr_rec_needs___9="0",
        mr_rec_needs___10="0",
        mr_rec_needs___11="0",
        mr_rec_needs___12="0",
        mr_rec_needs___13="0",
        mr_rec_needs___14="0",
        mr_rec_needs___15="0",
        mr_rec_needs___88="0",
        mr_rec_needs_inf___1="0",
        mr_rec_needs_inf___2="0",
        mr_rec_needs_inf___3="0",
        mr_rec_needs_inf___4="0",
        mr_rec_needs_inf___5="0",
        mr_rec_needs_inf___6="0",
        mr_rec_needs_inf___7="0",
        mr_rec_needs_inf___8="0",
        mr_rec_needs_inf___9="0",
        mr_rec_needs_inf___10="0",
        mr_rec_needs_inf___11="0",
        mr_rec_needs_inf___12="0",
        mr_rec_needs_inf___13="0",
        mr_rec_needs_inf___88="0"
    )
    print(data2.to_dict())
    template_service = TemplateService(template_path)
    template_service.fill_template(output_dir,data.record, data2.to_dict())

if __name__ == "__main__":
    generate_invoice_pdf()
