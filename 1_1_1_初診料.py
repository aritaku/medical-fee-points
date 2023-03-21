# 1_1_1 初診料

def calculate_initial_consultation_fee_v2(
    is_first_visit: bool,
    remote_first_visit: bool,
    facility_type: str,
    patient_referral_percentage: float,
    bed_count: int,
    medical_drug_trade_price_rate: float,
    meets_minister_criteria: bool,
    multiple_diseases_same_day: bool,
    is_infant: bool,
    consultation_time: str,
    is_pediatrics: bool,
):
    initial_consultation_fee = 0

    if is_first_visit:
        if remote_first_visit:
            initial_consultation_fee = 251
        else:
            initial_consultation_fee = 288

            if facility_type in ["特定機能病院", "地域医療支援病院", "外来機能報告対象病院等"]:
                if bed_count < 200 and patient_referral_percentage < meets_minister_criteria:
                    initial_consultation_fee = 214

            if facility_type == "病院":
                if 400 <= bed_count and patient_referral_percentage < meets_minister_criteria:
                    initial_consultation_fee = 214

                if 200 <= bed_count and meets_minister_criteria:
                    initial_consultation_fee = 214

        # Condition 5
        if multiple_diseases_same_day:
            initial_consultation_fee = 144

        # Condition 6
        if is_infant:
            initial_consultation_fee += 75

        # Condition 7
        if consultation_time == "outside_hours":
            initial_consultation_fee += 85
        elif consultation_time == "holiday":
            initial_consultation_fee += 250
        elif consultation_time == "late_night":
            initial_consultation_fee += 480

        if is_infant and consultation_time in ["outside_hours", "holiday", "late_night"]:
            initial_consultation_fee += 200 if consultation_time == "outside_hours" else 365 if consultation_time == "holiday" else 695

        # Condition 8
        if is_pediatrics and consultation_time in ["outside_hours", "holiday", "late_night"]:
            if is_infant:
                initial_consultation_fee += 200 if consultation_time == "outside_hours" else 365 if consultation_time == "holiday" else 695

        # Condition 9
        if meets_facility_criteria and consultation_time in ["evening", "early_morning"]:
            initial_consultation_fee += 50

        # Condition 10
        if facility_type in ["病院", "診療所"] and bed_count < 200 and meets_facility_criteria:
            initial_consultation_fee += 80

        # Condition 11
        if facility_type == "診療所" and minister_criterion_category == "infection_prevention":
            initial_consultation_fee += 6

        # Condition 12
        if facility_type == "診療所" and minister_criterion_category == "collaboration_strengthening":
            initial_consultation_fee += 3

        # Condition 13
        if facility_type == "診療所" and minister_criterion_category == "surveillance_strengthening":
            initial_consultation_fee += 1

        # Condition 14
        if uses_electronic_health_data:
            if health_data_difficult_to_obtain:
                initial_consultation_fee += 3
            else:
                initial_consultation_fee += 7

    return initial_consultation_fee
