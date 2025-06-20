from faker import Faker
import random
from datetime import datetime, timedelta
from models.redcap_response_second import RedcapResponseSecond
from models.redcap_response_first import RedcapResponseFirst
from utils.filters import filter_records
from typing import List
fake = Faker()

def generate_fake_detail_responses(mg_idpreg,count: int):
    return [generate_fake_detail_record(mg_idpreg) for i in range(count)]


def generate_fake_log_record():
    return {
            "timestamp": fake.date_time_this_year(),
            "username": fake.user_name(),
            "action": fake.word(),
            "details": fake.text(),
            "record": fake.uuid4()
        }
def generate_fake_log_responses(count: int):
    return [generate_fake_log_record() for i in range(count)]




def generate_fake_detail_record(mg_idpreg, count=1) -> List[RedcapResponseSecond]:
    """
    Generate fake records for REDCap maternal-infant health surveillance system
    """
    details = []
    
    for i in range(count):
        # Generate related dates
        lmp_date = fake.date_between(start_date="-1y", end_date="-40w")
        edd_date = lmp_date + timedelta(weeks=40)
        birth_date = fake.date_between(start_date=edd_date - timedelta(weeks=4), 
                                     end_date=edd_date + timedelta(weeks=2))
        pn_date = fake.date_between(start_date=lmp_date + timedelta(weeks=8), 
                                  end_date=lmp_date + timedelta(weeks=36))
        mr_request_dt = fake.date_between(start_date="-1y", end_date="today").isoformat()
        mr_request_dt_2 = fake.date_between(start_date="today", end_date="+6M").isoformat()
        
        # Generate baby ID
        bg_idbaby = f"B{random.randint(100000, 999999)}"
        
        record = {
            # Basic identifiers
            "mg_idpreg": mg_idpreg,
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
            
            # Maternal General Information
            "mg_desc": fake.sentence(nb_words=4),
            "mg_idpreg_sp": f"SP{random.randint(1000, 9999)}",
            "mg_mra_done": str(random.choice([0, 1])),
            "mg_ltfu": str(random.choice([0, 1])),
            "mg_ltfu_why": str(random.randint(1, 5)) if random.choice([True, False]) else "",
            "mg_ltfu_why_sp": fake.sentence() if random.choice([True, False]) else "",
            "mg_dob": fake.date_of_birth(minimum_age=18, maximum_age=45).isoformat(),
            
            # Race/Ethnicity
            "mg_desc_race": str(random.randint(1, 7)),
            "mg_race_aian": str(random.choice([0, 1])),
            "mg_race_asian": str(random.choice([0, 1])),
            "mg_race_baa": str(random.choice([0, 1])),
            "mg_race_mena": str(random.choice([0, 1])),
            "mg_race_nhopi": str(random.choice([0, 1])),
            "mg_race_wh": str(random.choice([0, 1])),
            "mg_race_oth": str(random.choice([0, 1])),
            "mg_ethn": str(random.randint(1, 3)),
            
            # Demographics
            "mg_edu": str(random.randint(1, 8)),
            "mg_zip": fake.zipcode(),
            "mg_co": str(random.randint(1, 100)),
            "mg_tract": f"{random.randint(1000, 9999)}.{random.randint(10, 99)}",
            
            # Physical measurements
            "mg_ht": str(random.randint(150, 180)),  # height in cm
            "mg_ppwt": str(random.randint(45, 120)),  # pre-pregnancy weight
            "mg_dewt": str(random.randint(50, 130)),  # delivery weight
            
            # Pre-pregnancy conditions
            "mg_desc_ppcon": str(random.randint(0, 1)),
            "mg_ppcon_diabetes": str(random.choice([0, 1])),
            "mg_cron_htn": str(random.choice([0, 1])),
            
            # Substance use
            "mg_sub_alc": str(random.choice([0, 1])),
            "mg_sub_tobacco": str(random.choice([0, 1])),
            
            # Pregnancy history
            "mg_gravidity": str(random.randint(1, 8)),
            "mg_parity": str(random.randint(0, 6)),
            "mg_lmp": lmp_date.isoformat(),
            "mg_edd": edd_date.isoformat(),
            
            # Prenatal care
            "mg_pn": str(random.choice([0, 1])),
            "mg_pn_dt": pn_date.isoformat() if random.choice([True, False]) else "",
            "mg_pn_num": str(random.randint(0, 15)),
            
            # Pregnancy conditions
            "mg_desc_pregcon": str(random.choice([0, 1])),
            "mg_pregcon_diabetes": str(random.choice([0, 1])),
            "mg_pregcon_eclamphtn": str(random.choice([0, 1])),
            "mg_pregcon_fgr": str(random.choice([0, 1])),
            
            # Hospital and outcomes
            "mg_hosp_yn": str(random.choice([0, 1])),
            "mg_death": str(random.choice([0, 1])),
            "mg_death_dt": fake.date_between(start_date=birth_date, end_date="today").isoformat() if random.randint(1, 100) <= 2 else "",
            "mg_death_dx": fake.sentence() if random.randint(1, 100) <= 2 else "",
            "mg_insur": str(random.randint(1, 6)),
            "mg_plurality_de": str(random.randint(1, 3)),
            "mg_decon_icu": str(random.choice([0, 1])),
            "mg_decon_icuadm_dt": fake.date_between(start_date=birth_date, end_date=birth_date + timedelta(days=7)).isoformat() if random.choice([True, False]) else "",
            
            # Maternal complications
            "mc_desc": fake.sentence(nb_words=6),
            "mc_yn": str(random.choice([0, 1])),
            "mc_idnndss": f"NNDSS{random.randint(100000, 999999)}",
            "mc_drugs": str(random.choice([0, 1])),
            "mc_sub_mj": str(random.choice([0, 1])),
            "mc_sub_op_rx": str(random.choice([0, 1])),
            "mc_sub_op_il": str(random.choice([0, 1])),
            "mc_sub_op_moud": str(random.choice([0, 1])),
            "mc_sub_meth": str(random.choice([0, 1])),
            "mc_sub_coc": str(random.choice([0, 1])),
            "mc_sub_oth": str(random.choice([0, 1])),
            "mc_sub_oth_sp": fake.word() if random.choice([True, False]) else "",
            
            # Legal/social
            "felony_info": str(random.choice([0, 1])),
            "jail_status": str(random.choice([0, 1])),
            "mc_jail": str(random.choice([0, 1])),
            "mc_homeless": str(random.choice([0, 1])),
            
            # Medical conditions
            "mc_dpdx": str(random.choice([0, 1])),
            "mc_dpdx_dt": fake.date_between(start_date="-2y", end_date="today").isoformat() if random.choice([True, False]) else "",
            "mc_tx": str(random.choice([0, 1])),
            "mc_hiv": str(random.choice([0, 1])),
            "mc_hbv": str(random.choice([0, 1])),
            "mc_chol": str(random.choice([0, 1])),
            "mc_chol_dt": fake.date_between(start_date=lmp_date, end_date=birth_date).isoformat() if random.choice([True, False]) else "",
            
            # Tests and procedures
            "mc_test_amnio": str(random.choice([0, 1])),
            "mc_fetalmonitor": str(random.choice([0, 1])),
            "mc_de_h": str(random.choice([0, 1])),
            "mc_de_prolong": str(random.choice([0, 1])),
            "mc_laceration": str(random.choice([0, 1])),
            
            "mg_notes": fake.text(max_nb_chars=200),
            "pregnant_person_form_complete": "2",
            
            # Baby General Information
            "bg_desc": fake.sentence(nb_words=4),
            "bg_idbaby": bg_idbaby,
            "bg_mra_done": str(random.choice([0, 1])),
            "bg_ltfu": str(random.choice([0, 1])),
            "bg_ltfu_why": str(random.randint(1, 5)) if random.choice([True, False]) else "",
            "bg_ltfu_why_sp": fake.sentence() if random.choice([True, False]) else "",
            
            # Birth outcomes
            "bg_detype": str(random.randint(1, 4)),
            "bg_outcome": str(random.randint(1, 5)),
            "bg_outcome_dt": birth_date.isoformat(),
            "bg_birvol": str(random.randint(250, 4500)),  # birth weight in grams
            "bg_ga_w": str(random.randint(24, 42)),  # gestational age weeks
            "bg_ga_d": str(random.randint(0, 6)),   # gestational age days
            "bg_sex": str(random.randint(1, 3)),
            
            # Physical examinations
            "bg_exm_yn": str(random.choice([0, 1])),
            "bg_desc_exm": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_gen": str(random.choice([0, 1])),
            "bg_exm_gen_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_heent": str(random.choice([0, 1])),
            "bg_exm_heent_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_cardio": str(random.choice([0, 1])),
            "bg_exm_cardio_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_lung": str(random.choice([0, 1])),
            "bg_exm_lung_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_abd": str(random.choice([0, 1])),
            "bg_exm_abd_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_gu": str(random.choice([0, 1])),
            "bg_exm_gu_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_muske": str(random.choice([0, 1])),
            "bg_exm_muske_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_neuro": str(random.choice([0, 1])),
            "bg_exm_neuro_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_skin": str(random.choice([0, 1])),
            "bg_exm_skin_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_exm_sp": fake.sentence() if random.choice([True, False]) else "",
            
            # Baby measurements
            "bg_lt": str(random.randint(35, 55)),  # length in cm
            "bg_wt": str(random.randint(1500, 4500)),  # weight in grams
            "bg_hc": str(random.randint(28, 38)),  # head circumference
            "bg_bstfed": str(random.choice([0, 1])),
            
            # Discharge and care
            "bg_dis_dt": (birth_date + timedelta(days=random.randint(1, 10))).isoformat(),
            "bg_dischargecare": str(random.randint(1, 5)),
            "bg_dischargecare_sp": fake.sentence() if random.choice([True, False]) else "",
            "bg_cps": str(random.choice([0, 1])),
            
            # Baby outcomes
            "bg_death": str(random.choice([0, 1])),
            "bg_death_dt": fake.date_between(start_date=birth_date, end_date="today").isoformat() if random.randint(1, 100) <= 5 else "",
            "bg_death_dx": fake.sentence() if random.randint(1, 100) <= 5 else "",
            "bg_icu": str(random.choice([0, 1])),
            "bg_icudis_dt": (birth_date + timedelta(days=random.randint(1, 30))).isoformat() if random.choice([True, False]) else "",
            
            # Hearing tests
            "bg_hear_oae": str(random.choice([0, 1])),
            "bg_hear_abr": str(random.choice([0, 1])),
            "bg_hear_unk": str(random.choice([0, 1])),
            
            # Baby complications
            "bc_desc": fake.sentence(),
            "bc_idnndss": f"NNDSS{random.randint(100000, 999999)}",
            "bc_nas": str(random.choice([0, 1])),
            
            "bg_notes": fake.text(max_nb_chars=200),
            "pregnancy_outcomes_and_birth_form_complete": "2",
            
            # Contact and facility information
            "ifu_fac_phone": fake.phone_number(),
            "ifu_fac_num": fake.phone_number(),
            "bc_momnamefirst": fake.first_name().upper(),
            "bc_momnamelast": fake.last_name().upper(),
            "bc_momssn": fake.ssn().replace("-", ""),
            "inf_dob_mom_tr": fake.date_of_birth(minimum_age=20, maximum_age=45).isoformat(),
            "hos_name_cat_2": str(random.randint(1, 10)),
            
            # Medical records requests
            "mr_request": "1",
            "mr_request_dt": mr_request_dt,
            "mr_request_days": str(random.randint(1, 100)),
            "mr_received": "1",
            "mr_rec_all":"1",
            "mr_rec_needs___4": "1",
            "mr_rec_needs___6": "1",
            "mr_rec_needs___7": "1",
            "mr_rec_needs___8": "1",
            "mr_rec_needs___9": "1",
            # Medical records requests 2
            "mr_request_2": "1",
            "mr_request_dt_2": mr_request_dt,
            "mr_request_days_2": str(random.randint(1, 100)),
            "mr_received_2": "1",
            "mr_rec_needs___4_2": "1",
            "mr_rec_needs___6_2": "1",
            
            # Hospital information
            "hos_name": fake.company() + " Hospital",
            "bc_birthplacename": fake.company() + " Medical Center",
            "hospital_address": fake.address(),
            "bc_birthplace_city_state": f"{fake.city()}, {fake.state_abbr()}",
            "bc_dattendant": fake.name(),
            "hospital_phone_num": fake.phone_number(),
            "hospital_fax_num": fake.phone_number(),
            "hospital_mr": f"MR{random.randint(100000, 999999)}",
            
            # Birth certificate information
            "year_cert_no": str(birth_date.year),
            "bc_childnamefirst": fake.first_name().upper(),
            "bc_childnamelast": fake.last_name().upper(),
            "dob_inf": birth_date.isoformat(),
            "bc_sex": str(random.randint(1, 2)),
            
            # Additional identifiers
            "mom_nbs_id": f"NBS{random.randint(100000, 999999)}",
            "infant_nbs_id": f"NBS{random.randint(100000, 999999)}",
            "con_inv_local_id": f"INV{random.randint(1000, 9999)}",
            
            # Form completion status
            "infant_follow_up_form_complete": str(random.randint(0, 2)),
            "diagnosis_code_form_complete": str(random.randint(0, 2)),
            "treatment_form_complete": str(random.randint(0, 2)),
            "pregnant_person_laboratory_form_complete": str(random.randint(0, 2)),
            "infant_laboratory_form_complete": str(random.randint(0, 2)),
            "hospital_and_pediatrician_information_complete": str(random.randint(0, 2)),
            "pregnant_person_information_complete": str(random.randint(0, 2)),
            "infant_information_complete": str(random.randint(0, 2)),
            "medical_records_request_for_pregnancy_and_birth_complete": str(random.randint(0, 2)),
        }
        
        details.append(record)
    filtered_details = filter_records(details, RedcapResponseSecond)
    return filtered_details

# Example usage:
if __name__ == "__main__":
    # Generate fake records for testing
    fake_records = generate_fake_detail_record("P123456", count=3)
    
    # Print first record as example
    import json
    print(json.dumps(fake_records[0], indent=2))