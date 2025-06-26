from dataclasses import dataclass, field, fields
import optparse
from typing import Any, Optional, Union
import re


@dataclass
class RedcapResponseSecond:
    # Core identifiers
    DELIVERY_DATE:Optional[str]=""
    mg_idpreg: Optional[str] = ""
    redcap_repeat_instrument: Optional[str] = ""
    redcap_repeat_instance: Optional[str] = ""
    
    # Maternal General Information
    mg_idpreg_sp: Optional[str] = ""
    mg_mra_done: Optional[str] = ""
    mg_ltfu: Optional[str] = ""
    mg_ltfu_why: Optional[str] = ""
    mg_ltfu_why_sp: Optional[str] = ""
    mg_dob: Optional[str] = ""
    
    # Maternal Race/Ethnicity
    mg_race_aian: Optional[str] = ""  # American Indian/Alaska Native
    mg_race_asian: Optional[str] = ""
    mg_race_baa: Optional[str] = ""   # Black/African American
    mg_race_mena: Optional[str] = ""  # Middle Eastern/North African
    mg_race_nhopi: Optional[str] = "" # Native Hawaiian/Other Pacific Islander
    mg_race_wh: Optional[str] = ""    # White
    mg_race_oth: Optional[str] = ""   # Other
    mg_ethn: Optional[str] = ""       # Ethnicity
    
    # Maternal Demographics
    mg_edu: Optional[str] = ""        # Education
    mg_zip: Optional[str] = ""
    mg_co: Optional[str] = ""         # County
    mg_tract: Optional[str] = ""      # Census tract
    
    # Maternal Physical Measurements
    mg_ht: Optional[str] = ""         # Height
    mg_ppwt: Optional[str] = ""       # Pre-pregnancy weight
    mg_dewt: Optional[str] = ""       # Delivery weight
    
    # Maternal Medical History
    mg_ppcon_diabetes: Optional[str] = ""     # Pre-pregnancy diabetes
    mg_cron_htn: Optional[str] = ""           # Chronic hypertension
    mg_sub_alc: Optional[str] = ""            # Alcohol use
    mg_sub_tobacco: Optional[str] = ""        # Tobacco use
    
    # Pregnancy Information
    mg_gravidity: Optional[str] = ""
    mg_parity: Optional[str] = ""
    mg_lmp: Optional[str] = ""        # Last menstrual period
    mg_edd: Optional[str] = ""        # Estimated due date
    mg_pn: Optional[str] = ""         # Prenatal care
    mg_pn_dt: Optional[str] = ""      # Prenatal care date
    mg_pn_num: Optional[str] = ""     # Number of prenatal visits
    
    # Pregnancy Complications
    mg_pregcon_diabetes: Optional[str] = ""    # Pregnancy diabetes
    mg_pregcon_eclamphtn: Optional[str] = ""   # Eclampsia/Hypertension
    mg_pregcon_fgr: Optional[str] = ""         # Fetal growth restriction
    
    # Maternal Outcomes
    mg_hosp_yn: Optional[str] = ""
    mg_death: Optional[str] = ""
    mg_death_dt: Optional[str] = ""
    mg_death_dx: Optional[str] = ""
    mg_insur: Optional[str] = ""      # Insurance
    mg_plurality_de: Optional[str] = "" # Multiple births
    mg_decon_icu: Optional[str] = "" # ICU admission
    mg_decon_icuadm_dt: Optional[str] = ""
    
    # Maternal Conditions (mc_ prefix)
    mc_yn: Optional[str] = ""
    mc_idnndss: Optional[str] = ""
    mc_drugs: Optional[str] = ""
    mc_sub_mj: Optional[str] = ""      # Marijuana
    mc_sub_op_rx: Optional[str] = ""   # Prescription opioids
    mc_sub_op_il: Optional[str] = ""   # Illegal opioids
    mc_sub_op_moud: Optional[str] = "" # Medication-assisted treatment
    mc_sub_meth: Optional[str] = ""    # Methamphetamine
    mc_sub_coc: Optional[str] = ""     # Cocaine
    mc_sub_oth: Optional[str] = ""     # Other substances
    mc_sub_oth_sp: Optional[str] = ""
    mc_jail: Optional[str] = ""
    mc_homeless: Optional[str] = ""
    mc_dpdx: Optional[str] = ""        # Depression diagnosis
    mc_dpdx_dt: Optional[str] = ""
    mc_tx: Optional[str] = ""          # Treatment
    mc_hiv: Optional[str] = ""
    mc_hbv: Optional[str] = ""         # Hepatitis B
    mc_chol: Optional[str] = ""        # Cholestasis
    mc_chol_dt: Optional[str] = ""
    mc_test_amnio: Optional[str] = ""  # Amniocentesis
    mc_fetalmonitor: Optional[str] = ""
    mc_de_h: Optional[str] = ""        # Delivery complications
    mc_de_prolong: Optional[str] = ""  # Prolonged labor
    mc_laceration: Optional[str] = ""
    mg_notes: Optional[str] = ""
    pregnant_person_form_complete: Optional[str] = ""
    
    # Baby General Information (bg_ prefix)
    bg_idbaby: Optional[str] = ""
    bg_mra_done: Optional[str] = ""
    bg_ltfu: Optional[str] = ""
    bg_ltfu_why: Optional[str] = ""
    bg_ltfu_why_sp: Optional[str] = ""
    bg_detype: Optional[str] = ""      # Delivery type
    bg_outcome: Optional[str] = ""
    bg_outcome_dt: Optional[str] = ""
    bg_birvol: Optional[str] = ""      # Birth volume
    bg_ga_w: Optional[str] = ""        # Gestational age weeks
    bg_ga_d: Optional[str] = ""        # Gestational age days
    bg_sex: Optional[str] = ""
    
    # Baby Physical Examination
    bg_exm_yn: Optional[str] = ""
    bg_exm_gen: Optional[str] = ""     # General examination
    bg_exm_gen_sp: Optional[str] = ""
    bg_exm_heent: Optional[str] = ""   # Head, eyes, ears, nose, throat
    bg_exm_heent_sp: Optional[str] = ""
    bg_exm_cardio: Optional[str] = ""  # Cardiovascular
    bg_exm_cardio_sp: Optional[str] = ""
    bg_exm_lung: Optional[str] = ""
    bg_exm_lung_sp: Optional[str] = ""
    bg_exm_abd: Optional[str] = ""     # Abdomen
    bg_exm_abd_sp: Optional[str] = ""
    bg_exm_gu: Optional[str] = ""      # Genitourinary
    bg_exm_gu_sp: Optional[str] = ""
    bg_exm_muske: Optional[str] = ""   # Musculoskeletal
    bg_exm_muske_sp: Optional[str] = ""
    bg_exm_neuro: Optional[str] = ""   # Neurological
    bg_exm_neuro_sp: Optional[str] = ""
    bg_exm_skin: Optional[str] = ""
    bg_exm_skin_sp: Optional[str] = ""
    bg_exm_sp: Optional[str] = ""
    
    # Baby Measurements
    bg_lt: Optional[str] = ""          # Length
    bg_wt: Optional[str] = ""          # Weight
    bg_hc: Optional[str] = ""          # Head circumference
    bg_bstfed: Optional[str] = ""      # Breastfed
    
    # Baby Discharge/Outcomes
    bg_dis_dt: Optional[str] = ""      # Discharge date
    bg_dischargecare: Optional[str] = ""
    bg_dischargecare_sp: Optional[str] = ""
    bg_cps: Optional[str] = ""         # Child Protective Services
    bg_death: Optional[str] = ""
    bg_death_dt: Optional[str] = ""
    bg_death_dx: Optional[str] = ""
    bg_icu: Optional[str] = ""
    bg_icudis_dt: Optional[str] = ""
    
    # Baby Hearing Tests
    bg_hear_oae: Optional[str] = ""    # Otoacoustic emissions
    bg_hear_abr: Optional[str] = ""    # Auditory brainstem response
    bg_hear_unk: Optional[str] = ""    # Unknown
    
    # Baby Conditions
    bc_idnndss: Optional[str] = ""
    bc_nas: Optional[str] = ""         # Neonatal abstinence syndrome
    bg_notes: Optional[str] = ""
    pregnancy_outcomes_and_birth_form_complete: Optional[str] = ""
    
    # Infant Follow-up (ig_ prefix)
    ig_idbaby: Optional[str] = ""
    ig_mra_done: Optional[str] = ""
    ig_ltfu: Optional[str] = ""
    ig_ltfu_why: Optional[str] = ""
    ig_ltfu_why_sp: Optional[str] = ""
    ig_death: Optional[str] = ""
    ig_death_dt: Optional[str] = ""
    ig_death_dx: Optional[str] = ""
    ig_livingwith: Optional[str] = ""
    ig_livingwith_sp: Optional[str] = ""
    ig_cps: Optional[str] = ""
    ig_visit_dt: Optional[str] = ""
    
    # Infant Follow-up Examination
    ig_exm_yn: Optional[str] = ""
    ig_exm_gen: Optional[str] = ""
    ig_exm_gen_sp: Optional[str] = ""
    ig_exm_heent: Optional[str] = ""
    ig_exm_heent_sp: Optional[str] = ""
    ig_exm_cardio: Optional[str] = ""
    ig_exm_cardio_sp: Optional[str] = ""
    ig_exm_lung: Optional[str] = ""
    ig_exm_lung_sp: Optional[str] = ""
    ig_exm_abd: Optional[str] = ""
    ig_exm_abd_sp: Optional[str] = ""
    ig_exm_gu: Optional[str] = ""
    ig_exm_gu_sp: Optional[str] = ""
    ig_exm_muske: Optional[str] = ""
    ig_exm_muske_sp: Optional[str] = ""
    ig_exm_neuro: Optional[str] = ""
    ig_exm_neuro_sp: Optional[str] = ""
    ig_exm_skin: Optional[str] = ""
    ig_exm_skin_sp: Optional[str] = ""
    ig_exm_sp: Optional[str] = ""
    
    # Infant Follow-up Measurements
    ig_lt: Optional[str] = ""
    ig_wt: Optional[str] = ""
    ig_hc: Optional[str] = ""
    ig_bstfed: Optional[str] = ""
    
    # Referrals
    ig_ref_ei: Optional[str] = ""      # Early intervention
    ig_ref_pt: Optional[str] = ""      # Physical therapy
    ig_ref_ot: Optional[str] = ""      # Occupational therapy
    ig_ref_slp: Optional[str] = ""     # Speech-language pathology
    ig_ref_opth: Optional[str] = ""    # Ophthalmology
    ig_ref_audio: Optional[str] = ""   # Audiology
    ig_ref_dev: Optional[str] = ""     # Developmental
    ig_ref_med: Optional[str] = ""     # Medical
    ig_ref_oth: Optional[str] = ""     # Other
    ig_ref_med_sp: Optional[str] = ""
    ig_ref_oth_sp: Optional[str] = ""
    
    # Specialist Visits
    ig_opth: Optional[str] = ""        # Ophthalmology visit
    ig_opth_dt: Optional[str] = ""
    ig_opth_res: Optional[str] = ""    # Results
    ig_opth_sp: Optional[str] = ""
    ig_audio: Optional[str] = ""       # Audiology visit
    ig_audio_dt: Optional[str] = ""
    ig_audio_res: Optional[str] = ""
    ig_audio_chl: Optional[str] = ""   # Conductive hearing loss
    ig_audio_snhl: Optional[str] = ""  # Sensorineural hearing loss
    ig_audio_ansd: Optional[str] = ""  # Auditory neuropathy spectrum disorder
    ig_audio_oth: Optional[str] = ""
    ig_audio_oth_sp: Optional[str] = ""
    
    # Infant Conditions
    ic_liver: Optional[str] = ""
    ic_liver_dx: Optional[str] = ""
    ic_liver_dt: Optional[str] = ""
    ic_tx: Optional[str] = ""
    ig_notes: Optional[str] = ""
    infant_follow_up_form_complete: Optional[str] = ""
    
    # Infant Follow-up Administration
    abs_who_ifu: Optional[str] = ""
    ifu_fac_name: Optional[str] = ""
    ifu_fac_phone: Optional[str] = ""
    ifu_fac_city: Optional[str] = ""
    ifu_fac_num: Optional[str] = ""
    ifu_varify_who: Optional[str] = ""
    ifu_fac_notes: Optional[str] = ""
    
    # Request tracking
    request_ifu: Optional[str] = ""
    req_date_ifu: Optional[str] = ""
    req_ifu_days: Optional[str] = ""
    request2_ifu: Optional[str] = ""
    req2_date_ifu: Optional[str] = ""
    req2_ifu_days: Optional[str] = ""
    ifu_record: Optional[str] = ""
    mr_ifu_rec_date: Optional[str] = ""
    request_ifu_2: Optional[str] = ""
    req_date_ifu_2: Optional[str] = ""
    req_ifu_days_2: Optional[str] = ""
    request2_ifu_2: Optional[str] = ""
    req2_date_ifu_2: Optional[str] = ""
    req2_ifu_days_2: Optional[str] = ""
    ifu_record_2: Optional[str] = ""
    mr_ifu_rec_date_2: Optional[str] = ""
    ifu_requester_notes: Optional[str] = ""

    
    # File uploads
    file_upload_v2: Optional[str] = ""
    file_upload_2_v2: Optional[str] = ""
    file_upload_3_v2: Optional[str] = ""
    file_upload_4_v2: Optional[str] = ""
    
    # Case management
    case_assignment_ifu: Optional[str] = ""
    chart_abs_complete_ifu: Optional[str] = ""
    chart_abs_complete_ifu_2: Optional[str] = ""
    issue_rec_type_ifu___1: Optional[str] = ""
    issue_rec_type_ifu___2: Optional[str] = ""
    char_ab_issue_yn_ifu: Optional[str] = ""
    chart_ab_issue_txt_ifu: Optional[str] = ""
    rd_request_ifu_dt: Optional[str] = ""
    rd_req_days_ifu: Optional[str] = ""
    char_ab_issue_res_ifu: Optional[str] = ""
    char_ab_issue_res_ifu_ab: Optional[str] = ""
    ifu_bg_complete: Optional[str] = ""
    
    # Diagnosis Information (dg_ prefix)
    dg_idbaby: Optional[str] = ""
    dg_encount_dt: Optional[str] = ""
    dc_diag_timepoint: Optional[str] = ""
    dg_icd_code: Optional[str] = ""
    dg_macdp_code: Optional[str] = ""
    dg_diag_sp: Optional[str] = ""
    diagnosis_code_form_complete: Optional[str] = ""
    
    # Treatment Information (tc_ prefix)
    tc_idbaby: Optional[str] = ""
    tc_level: Optional[str] = ""
    tc_type: Optional[str] = ""
    tc_type_sp: Optional[str] = ""
    tc_st_dt: Optional[str] = ""       # Start date
    tc_end_dt: Optional[str] = ""      # End date
    tc_dose_sp: Optional[str] = ""
    treatment_form_complete: Optional[str] = ""
    
    # Laboratory - Pregnant Person (lc_prg_ prefix)
    lc_prg_test: Optional[str] = ""
    lc_prg_dt: Optional[str] = ""
    lc_prg_resinterp: Optional[str] = "" # Result interpretation
    lc_prg_quant: Optional[str] = ""     # Quantitative result
    lc_prg_quant_unit: Optional[str] = ""
    lc_prg_quant_unit_sp: Optional[str] = ""
    lc_prg_quant_ll: Optional[str] = ""  # Lower limit
    lc_prg_naat_geno: Optional[str] = "" # NAAT genotype
    lc_prg_snomed: Optional[str] = ""
    lc_prg_loinc: Optional[str] = ""
    p_lab_rpt_local_id: Optional[str] = ""
    lc_prg_notes: Optional[str] = ""
    pregnant_person_laboratory_form_complete: Optional[str] = ""
    
    # Laboratory - Infant (lc_inf_ prefix)
    lc_inf_idbaby: Optional[str] = ""
    lc_inf_test: Optional[str] = ""
    lc_inf_dt: Optional[str] = ""
    lc_inf_resinterp: Optional[str] = ""
    lc_inf_quant: Optional[str] = ""
    lc_inf_quant_unit: Optional[str] = ""
    lc_inf_quant_unit_sp: Optional[str] = ""
    lc_inf_quant_ll: Optional[str] = ""  # Lower limit
    lc_inf_quant_ul: Optional[str] = ""  # Upper limit
    lc_inf_snomed: Optional[str] = ""
    lc_inf_loinc: Optional[str] = ""
    i_lab_rpt_local_id: Optional[str] = ""
    lc_inf_notes: Optional[str] = ""
    infant_laboratory_form_complete: Optional[str] = ""
    
    # Hospital and Provider Information (dr_ prefix)
    dr_idbaby: Optional[str] = ""
    hos_name: Optional[str] = ""
    hos_name_cat: Optional[str] = ""
    bc_birthplacename: Optional[str] = ""
    hospital_address: Optional[str] = ""
    bc_birthplace_city_state: Optional[str] = ""
    bc_dattendant: Optional[str] = ""   # Birth attendant
    hospital_phone_num: Optional[str] = ""
    hospital_fax_num: Optional[str] = ""
    hospital_mr: Optional[str] = ""     # Medical record number
    hospital_mr_vr: Optional[str] = ""  # Vital records
    phys_name: Optional[str] = ""       # Physician name
    physician_phone_num: Optional[str] = ""
    physician_fax_num: Optional[str] = ""
    physician_address: Optional[str] = ""
    ped_notes: Optional[str] = ""
    hospital_and_pediatrician_information_complete: Optional[str] = ""
    
    # Birth Certificate Information
    year_cert_no: Optional[str] = ""
    mom_nbs_id: Optional[str] = ""      # Newborn screening ID
    con_inv_local_id: Optional[str] = ""
    bc_momnamefirst: Optional[str] = ""
    bc_momnamemiddle: Optional[str] = ""
    bc_momnamelast: Optional[str] = ""
    bc_momnamemaidenlast: Optional[str] = ""
    bc_mom_dob: Optional[str] = ""
    bc_momssn: Optional[str] = ""
    inf_dob_mom_tr: Optional[str] = ""  # Infant DOB from mother's record
    mom_death_ind: Optional[str] = ""
    mom_dod_cert_num: Optional[str] = ""
    mom_ddod: Optional[str] = ""        # Date of death
    mom_dcause: Optional[str] = ""      # Cause of death
    con_inv_case_status: Optional[str] = ""
    mom_demo_notes: Optional[str] = ""
    pregnant_person_information_complete: Optional[str] = ""
    
    # Infant Demographics
    id_idbaby: Optional[str] = ""
    inf_dem_bc_number: Optional[str] = ""
    infant_nbs_id: Optional[str] = ""
    pinv_inv_local_id: Optional[str] = ""
    bc_childnamefirst: Optional[str] = ""
    bc_childnamemiddle: Optional[str] = ""
    bc_childnamelast: Optional[str] = ""
    dob_inf: Optional[str] = ""
    bc_sex: Optional[str] = ""
    bc_childssn: Optional[str] = ""
    inf_death_ind: Optional[str] = ""
    dcertnum: Optional[str] = ""        # Death certificate number
    ddod: Optional[str] = ""            # Date of death
    dcause: Optional[str] = ""          # Cause of death
    pinv_inv_case_status: Optional[str] = ""
    inf_demo_notes: Optional[str] = ""
    infant_information_complete: Optional[str] = ""
    
    # Medical Records Management
    hos_name_cat_2: Optional[str] = ""
    year_of_birth: Optional[str] = ""
    mr_emr: Optional[str] = ""          # Electronic medical record
    emr_used: Optional[str] = ""
    emr_notes: Optional[str] = ""
    mr_emg_all: Optional[str] = ""      # All emergency records
    
        # Medical Record Needs (Checkboxes - multiple values possible)
    mr_emr_needs___1: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___2: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___3: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___4: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___5: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___6: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___7: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___8: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___9: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___10: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___11: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___12: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___13: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___14: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___15: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs___88: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_oth: Optional[str] = ""

    # Infant Medical Record Needs
    mr_emr_needs_inf___1: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___2: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___3: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___4: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___5: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___6: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___7: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___8: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___9: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___10: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___11: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___12: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___13: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_inf___88: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_emr_needs_oth_inf: Optional[str] = ""

    mr_req_for: Optional[str] = ""
    # First Medical Record Request
    mr_request: Optional[str] = ""
    mr_request_dt: Optional[str] = ""
    mr_request_days: Optional[str] = ""
    mr_received: Optional[str] = ""
    record_rec_via: Optional[str] = ""
    mr_rec_all: Optional[str] = ""

    # First Request - Records Received
    mr_rec_needs___1: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___2: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___3: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___4: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___6: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___7: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___8: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___9: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___10: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___11: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___12: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___13: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___14: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___15: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs___88: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_needs_oth: Optional[str] = field(default="", metadata={"prefix": True, "prefix_str": ""})

    # First Request - Infant Records Received
    mr_rec_needs_inf___1:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___2:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___3:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___4:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___5:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___6:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___7:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___8:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___9:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___10:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___11:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___12:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___13:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf___88:  Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_needs_oth_inf:  Optional[str] = field(default="", metadata={"prefix": True, "prefix_str": ""})
    attestation:  Optional[Any] = field(default="", metadata={"checkbox": True})

    # Second Medical Record Request
    mr_request_2: Optional[str] = ""
    mr_request_dt_2: Optional[str] = ""
    mr_request_days_2: Optional[str] = ""
    mr_received_2: Optional[str] = ""
    record_rec_via_2: Optional[str] = ""
    mr_rec_all_2: Optional[str] = ""

    # Second Request - Records Received
    mr_rec_needs_2___1: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___2: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___3: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___4: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___6: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___7: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___8: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___9: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___10: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___11: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___12: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___13: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___14: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___15: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_2___88: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_needs_oth_2: Optional[str] = ""
    
    # Second Request - Infant Records Received
    mr_rec_needs_inf_2___1: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___2: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___3: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___4: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___5: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___6: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___7: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___8: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___9: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___10: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___11: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___12: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___13: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_rec_needs_inf_2___88: Optional[Any] = field(default="", metadata={"checkbox": True})
    mr_needs_oth_inf_2: Optional[str] = ""
    
    # Final tracking fields
    ltfu: Optional[str] = ""            # Lost to follow-up
    mra_pass: Optional[str] = ""        # Medical record abstraction pass
    mr_upload: Optional[str] = ""       # Medical record uploads
    mr_upload_2: Optional[str] = ""
    mr_upload_3: Optional[str] = ""
    mr_upload_4: Optional[str] = ""
    mr_upload_5: Optional[str] = ""
    medical_records_request_for_pregnancy_and_birth_complete:Optional[str] = ""

    def __post_init__(self):
        for f in fields(self):
            if f.metadata.get("checkbox"):
                val = getattr(self, f.name)
                if val in [1, "1", True]:
                    setattr(self, f.name, "☑")
                else:
                    setattr(self, f.name, "☐")
            if f.metadata.get("prefix"):
                val = getattr(self, f.name)
                if val:
                    setattr(self, f.name, f'{f.metadata.get("prefix_str")} {val}')

    def to_dict(self):
        """Convert the dataclass instance to a dictionary."""
        return {

            "mg_idpreg": self.mg_idpreg,
            "DELIVERY_DATE": self.DELIVERY_DATE,
            "hospital_phone_num": self.hospital_phone_num,
            "hospital_fax_num": self.hospital_fax_num,
            "hospital_mr": self.hospital_mr,
            "hospital_mr_vr": self.hospital_mr_vr,
            "phys_name": self.phys_name,
            "physician_phone_num": self.physician_phone_num,
            "physician_fax_num": self.physician_fax_num,
            "redcap_repeat_instrument": self.redcap_repeat_instrument,
            "redcap_repeat_instance": self.redcap_repeat_instance,
            "mg_idpreg_sp": self.mg_idpreg_sp,
            "mg_mra_done": self.mg_mra_done,
            "mg_ltfu": self.mg_ltfu,
            "mg_ltfu_why": self.mg_ltfu_why,
            "mg_ltfu_why_sp": self.mg_ltfu_why_sp,
            "mg_dob": self.mg_dob,
            "mg_race_aian": self.mg_race_aian,
            "mg_race_asian": self.mg_race_asian,
            "mg_race_baa": self.mg_race_baa,
            "mg_race_mena": self.mg_race_mena,
            "mg_race_nhopi": self.mg_race_nhopi,
            "mg_race_wh": self.mg_race_wh,
            "mg_race_oth": self.mg_race_oth,
            "mg_ethn": self.mg_ethn,
            "mg_edu": self.mg_edu,
            "mg_zip": self.mg_zip,
            "mg_co": self.mg_co,
            "mg_tract": self.mg_tract,
            "mg_ht": self.mg_ht,
            "mg_ppwt": self.mg_ppwt,
            "mg_dewt": self.mg_dewt,
            "mg_ppcon_diabetes": self.mg_ppcon_diabetes,
            "mg_cron_htn": self.mg_cron_htn,
            "mg_sub_alc": self.mg_sub_alc,
            "mg_sub_tobacco": self.mg_sub_tobacco,
            "mg_gravidity": self.mg_gravidity,
            "mg_parity": self.mg_parity,
            "mg_lmp": self.mg_lmp,
            "mg_edd": self.mg_edd,
            "mg_pn": self.mg_pn,
            "mg_pn_dt": self.mg_pn_dt,
            "mg_pn_num": self.mg_pn_num,
            "mg_pregcon_diabetes": self.mg_pregcon_diabetes,
            "mg_pregcon_eclamphtn": self.mg_pregcon_eclamphtn,
            "mg_pregcon_fgr": self.mg_pregcon_fgr,
            "mg_hosp_yn": self.mg_hosp_yn,
            "mg_death": self.mg_death,
            "mg_death_dt": self.mg_death_dt,
            "mg_death_dx": self.mg_death_dx,
            "mg_insur": self.mg_insur,
            "mg_plurality_de": self.mg_plurality_de,
            "mg_decon_icu": self.mg_decon_icu,
            "mg_decon_icuadm_dt": self.mg_decon_icuadm_dt,
            "mc_yn": self.mc_yn,
            "mc_idnndss": self.mc_idnndss,
            "mc_drugs": self.mc_drugs,
            "mc_sub_mj": self.mc_sub_mj,
            "mc_sub_op_rx": self.mc_sub_op_rx,
            "mc_sub_op_il": self.mc_sub_op_il,
            "mc_sub_op_moud": self.mc_sub_op_moud,
            "mc_sub_meth": self.mc_sub_meth,
            "mc_sub_coc": self.mc_sub_coc,
            "mc_sub_oth": self.mc_sub_oth,
            "mc_sub_oth_sp": self.mc_sub_oth_sp,
            "mc_jail": self.mc_jail,
            "mc_homeless": self.mc_homeless,
            "mc_dpdx": self.mc_dpdx,
            "mc_dpdx_dt": self.mc_dpdx_dt,
            "mc_tx": self.mc_tx,
            "mc_hiv": self.mc_hiv,
            "mc_hbv": self.mc_hbv,
            "mc_chol": self.mc_chol,
            "mc_chol_dt": self.mc_chol_dt,
            "mc_test_amnio": self.mc_test_amnio,
            "mc_fetalmonitor": self.mc_fetalmonitor,
            "mc_de_h": self.mc_de_h,
            "mc_de_prolong": self.mc_de_prolong,
            "mc_laceration": self.mc_laceration,
            "mg_notes": self.mg_notes,
            "pregnant_person_form_complete": self.pregnant_person_form_complete,
            "bg_idbaby": self.bg_idbaby,
            "bg_mra_done": self.bg_mra_done,
            "bg_ltfu": self.bg_ltfu,
            "bg_ltfu_why": self.bg_ltfu_why,
            "bg_ltfu_why_sp": self.bg_ltfu_why_sp,
            "bg_detype": self.bg_detype,
            "bg_outcome": self.bg_outcome,
            "bg_outcome_dt": self.bg_outcome_dt,
            "bg_birvol": self.bg_birvol,
            "bg_ga_w": self.bg_ga_w,
            "bg_ga_d": self.bg_ga_d,
            "bg_sex": self.bg_sex,
            "bg_exm_yn": self.bg_exm_yn,
            "bg_exm_gen": self.bg_exm_gen,
            "bg_exm_gen_sp": self.bg_exm_gen_sp,
            "bg_exm_heent": self.bg_exm_heent,
            "bg_exm_heent_sp": self.bg_exm_heent_sp,
            "bg_exm_cardio": self.bg_exm_cardio,
            "bg_exm_cardio_sp": self.bg_exm_cardio_sp,
            "bg_exm_lung": self.bg_exm_lung,
            "bg_exm_lung_sp": self.bg_exm_lung_sp,
            "bg_exm_abd": self.bg_exm_abd,
            "bg_exm_abd_sp": self.bg_exm_abd_sp,
            "bg_exm_gu": self.bg_exm_gu,
            "bg_exm_gu_sp": self.bg_exm_gu_sp,
            "bg_exm_muske": self.bg_exm_muske,
            "bg_exm_muske_sp": self.bg_exm_muske_sp,
            "bg_exm_neuro": self.bg_exm_neuro,
            "bg_exm_neuro_sp": self.bg_exm_neuro_sp,
            "bg_exm_skin": self.bg_exm_skin,
            "bg_exm_skin_sp": self.bg_exm_skin_sp,
            "bg_exm_sp": self.bg_exm_sp,
            "bg_lt": self.bg_lt,
            "bg_wt": self.bg_wt,
            "bg_hc": self.bg_hc,
            "bg_bstfed": self.bg_bstfed,
            "bg_dis_dt": self.bg_dis_dt,
            "bg_dischargecare": self.bg_dischargecare,
            "bg_dischargecare_sp": self.bg_dischargecare_sp,
            "bg_cps": self.bg_cps,
            "bg_death": self.bg_death,
            "bg_death_dt": self.bg_death_dt,
            "bg_death_dx": self.bg_death_dx,
            "bg_icu": self.bg_icu,
            "bg_icudis_dt": self.bg_icudis_dt,
            "bg_hear_oae": self.bg_hear_oae,
            "bg_hear_abr": self.bg_hear_abr,
            "bg_hear_unk": self.bg_hear_unk,
            "bc_momnamefirst": self.bc_momnamefirst,
            "bc_momnamelast": self.bc_momnamelast,
            "bc_mom_dob":self.bc_mom_dob,
            "bc_momssn": self.bc_momssn[-4:] if self.bc_momssn else "",
            "bc_childnamefirst": self.bc_childnamefirst,
            "bc_childnamelast": self.bc_childnamelast,
            "bc_childssn": self.bc_childssn[-4:] if self.bc_childssn else "",
            "inf_dob_mom_tr": self.inf_dob_mom_tr,
            "hos_name_cat_2": self.hos_name_cat_2,

            "mr_req_for" : self.mr_req_for,
            "mr_request": self.mr_request,
            "mr_request_dt": self.mr_request_dt,
            "mr_request_days": self.mr_request_days,
            "mr_received": self.mr_received,
            "mr_rec_all": self.mr_rec_all,

            "mr_request_2": self.mr_request_2,
            "mr_request_dt_2": self.mr_request_dt_2,
            'mr_received_2': self.mr_received_2,
            "mr_rec_all_2": self.mr_rec_all_2,

            "mr_rec_needs___1": self.mr_rec_needs___1,
            "mr_rec_needs___2": self.mr_rec_needs___2,
            "mr_rec_needs___3": self.mr_rec_needs___3,
            "redcap_repeat_instrument": self.redcap_repeat_instrument,
            "redcap_repeat_instance": self.redcap_repeat_instance,
            "ifu_fac_phone": self.ifu_fac_phone,
            "ifu_fac_num": self.ifu_fac_num,
            "mr_rec_needs___4": self.mr_rec_needs___4,
            "mr_rec_needs___6": self.mr_rec_needs___6,
            "mr_rec_needs___7": self.mr_rec_needs___7,
            "mr_rec_needs___8": self.mr_rec_needs___8,
            "mr_rec_needs___9": self.mr_rec_needs___9,
            "mr_rec_needs___10": self.mr_rec_needs___10,
            "mr_rec_needs___11": self.mr_rec_needs___11,
            "mr_rec_needs___12": self.mr_rec_needs___12,
            "mr_rec_needs___13": self.mr_rec_needs___13,
            "mr_rec_needs___14": self.mr_rec_needs___14,
            "mr_rec_needs___15": self.mr_rec_needs___15,
            "mr_rec_needs___88": self.mr_rec_needs___88,
            "mr_needs_oth": self.mr_needs_oth,
            "mr_rec_needs_inf___1": self.mr_rec_needs_inf___1,
            "mr_rec_needs_inf___2": self.mr_rec_needs_inf___2,
            "mr_rec_needs_inf___3": self.mr_rec_needs_inf___3,
            "mr_rec_needs_inf___4": self.mr_rec_needs_inf___4,
            "mr_rec_needs_inf___5": self.mr_rec_needs_inf___5,
            "mr_rec_needs_inf___6": self.mr_rec_needs_inf___6,
            "mr_rec_needs_inf___7": self.mr_rec_needs_inf___7,
            "mr_rec_needs_inf___8": self.mr_rec_needs_inf___8,
            "mr_rec_needs_inf___9": self.mr_rec_needs_inf___9,
            "mr_rec_needs_inf___10": self.mr_rec_needs_inf___10,
            "mr_rec_needs_inf___11": self.mr_rec_needs_inf___11,
            "mr_rec_needs_inf___12": self.mr_rec_needs_inf___12,
            "mr_rec_needs_inf___13": self.mr_rec_needs_inf___13,
            "mr_rec_needs_inf___88": self.mr_rec_needs_inf___88,
            "mr_needs_oth_inf": self.mr_needs_oth_inf,
            "mr_emr_needs___1": self.mr_emr_needs___1,
            "mr_emr_needs___2": self.mr_emr_needs___2,
            "mr_emr_needs___3": self.mr_emr_needs___3,
            "mr_emr_needs___4": self.mr_emr_needs___4,
            "mr_emr_needs___5": self.mr_emr_needs___5,
            "mr_emr_needs___6": self.mr_emr_needs___6,
            "mr_emr_needs___7": self.mr_emr_needs___7,
            "mr_emr_needs___8": self.mr_emr_needs___8,
            "mr_emr_needs___9": self.mr_emr_needs___9,
            "mr_emr_needs___10": self.mr_emr_needs___10,
            "mr_emr_needs___11": self.mr_emr_needs___11,
            "mr_emr_needs___12": self.mr_emr_needs___12,
            "mr_emr_needs___13": self.mr_emr_needs___13,
            "mr_emr_needs___88": self.mr_emr_needs___88,
            "mr_emr_needs_inf___1": self.mr_emr_needs_inf___1,
            "mr_emr_needs_inf___2": self.mr_emr_needs_inf___2,
            "mr_emr_needs_inf___3": self.mr_emr_needs_inf___3,
            "mr_emr_needs_inf___4": self.mr_emr_needs_inf___4,
            "mr_emr_needs_inf___5": self.mr_emr_needs_inf___5,
            "mr_emr_needs_inf___6": self.mr_emr_needs_inf___6,
            "mr_emr_needs_inf___7": self.mr_emr_needs_inf___7,
            "mr_emr_needs_inf___8": self.mr_emr_needs_inf___8,
            "mr_emr_needs_inf___9": self.mr_emr_needs_inf___9,
            "mr_emr_needs_inf___10": self.mr_emr_needs_inf___10,
            "mr_emr_needs_inf___11": self.mr_emr_needs_inf___11,
            "mr_emr_needs_inf___12": self.mr_emr_needs_inf___12,
            "mr_emr_needs_inf___13": self.mr_emr_needs_inf___13,
            "mr_emr_needs_inf___88": self.mr_emr_needs_inf___88,
            "hos_name": self.hos_name,
            "dob_inf" :self.dob_inf,
            "bc_childssn":self.bc_childssn[-4:] if self.bc_childssn else "" ,
            "bc_momnamemaidenlast":self.bc_momnamemaidenlast
}
    