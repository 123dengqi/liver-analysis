from __future__ import annotations

SUPPORTED_LANGS = frozenset({"zh", "en"})

STRINGS: dict[str, dict[str, str]] = {
    "zh": {
        "strategy_first": "首次住院记录",
        "strategy_latest": "末次住院记录",
        "strategy_all": "全部住院记录（每行独立）",
        "polypharmacy_definition": "出院药物种类≥{threshold}",
        "malnutrition_definition": "RFH-NPT≥{threshold}",
        "severity_measure": "MELD-Na评分",
        "analysis_unit_note": "每条住院记录作为独立分析单元；首次/末次策略每位患者仅保留一条记录。",
        "var_age": "年龄，岁",
        "var_male": "男性",
        "var_bmi": "BMI，kg/m²",
        "var_medication_count": "用药数量，种",
        "var_polypharmacy": "多重用药（≥{threshold}种）",
        "var_rfh_npt": "RFH-NPT评分",
        "var_high_malnutrition_risk": "高营养不良风险（RFH-NPT≥{threshold}）",
        "var_meld_na": "MELD-Na评分",
        "var_albumin": "白蛋白，g/L",
        "var_hemoglobin": "血红蛋白，g/L",
        "var_length_of_stay": "住院天数",
        "var_etiology_viral": "病毒性病因",
        "var_etiology_alcohol": "酒精性病因",
        "var_ascites": "腹水",
        "var_varices": "静脉曲张",
        "var_hepatic_encephalopathy": "肝性脑病",
        "var_infection": "感染",
        "var_diabetes": "糖尿病",
        "var_hypertension": "高血压",
        "var_coronary_heart_disease": "冠状动脉性心脏病",
        "group_no_polypharmacy": "非多重用药",
        "group_polypharmacy": "多重用药",
        "group_low_risk": "低风险",
        "group_high_risk": "高风险",
        "model_unadjusted": "未调整",
        "model_adjusted": "多变量调整",
        "term_polypharmacy": "多重用药（≥{threshold}种）",
        "term_age": "年龄（每增加1岁）",
        "term_sex_male": "男性",
        "term_bmi": "BMI（每增加1 kg/m²）",
        "term_meld_na": "MELD-Na（每增加1分）",
        "term_ascites": "腹水",
        "term_varices": "静脉曲张",
        "term_hepatic_encephalopathy": "肝性脑病",
        "term_infection": "感染",
        "term_diabetes": "糖尿病",
        "term_hypertension": "高血压",
        "term_coronary_heart_disease": "冠状动脉性心脏病",
        "term_etiology_prefix": "病因：",
        "adjustment_factors": "年龄、性别、BMI、病因、MELD-Na、并发症（腹水、静脉曲张、肝性脑病、感染）和合并症（糖尿病、高血压、冠状动脉性心脏病）",
        "variance_standard": "常规模型标准误",
        "variance_cluster": "按患者聚类的稳健标准误",
        "model_status_failed": "模型未能收敛",
        "etiology_unclassified": "未分类",
        "etiology_mixed": "混合病因",
        "etiology_viral": "病毒性",
        "etiology_cholestatic": "胆汁淤积性",
        "etiology_autoimmune": "自身免疫性",
        "etiology_alcohol": "酒精性",
    },
    "en": {
        "strategy_first": "First admission",
        "strategy_latest": "Latest admission",
        "strategy_all": "All admissions (row-independent)",
        "polypharmacy_definition": "Discharge medications ≥{threshold} types",
        "malnutrition_definition": "RFH-NPT ≥{threshold}",
        "severity_measure": "MELD-Na score",
        "analysis_unit_note": "Each admission record is treated as an independent unit; first/latest strategies keep one record per patient.",
        "var_age": "Age, years",
        "var_male": "Male",
        "var_bmi": "BMI, kg/m²",
        "var_medication_count": "Medication count",
        "var_polypharmacy": "Polypharmacy (≥{threshold} types)",
        "var_rfh_npt": "RFH-NPT score",
        "var_high_malnutrition_risk": "High malnutrition risk (RFH-NPT ≥{threshold})",
        "var_meld_na": "MELD-Na score",
        "var_albumin": "Albumin, g/L",
        "var_hemoglobin": "Hemoglobin, g/L",
        "var_length_of_stay": "Length of stay, days",
        "var_etiology_viral": "Viral etiology",
        "var_etiology_alcohol": "Alcoholic etiology",
        "var_ascites": "Ascites",
        "var_varices": "Varices",
        "var_hepatic_encephalopathy": "Hepatic encephalopathy",
        "var_infection": "Infection",
        "var_diabetes": "Diabetes",
        "var_hypertension": "Hypertension",
        "var_coronary_heart_disease": "Coronary heart disease",
        "group_no_polypharmacy": "No polypharmacy",
        "group_polypharmacy": "Polypharmacy",
        "group_low_risk": "Low risk",
        "group_high_risk": "High risk",
        "model_unadjusted": "Unadjusted",
        "model_adjusted": "Multivariable adjustment",
        "term_polypharmacy": "Polypharmacy (≥{threshold} types)",
        "term_age": "Age (per year)",
        "term_sex_male": "Male",
        "term_bmi": "BMI (per 1 kg/m²)",
        "term_meld_na": "MELD-Na (per 1 point)",
        "term_ascites": "Ascites",
        "term_varices": "Varices",
        "term_hepatic_encephalopathy": "Hepatic encephalopathy",
        "term_infection": "Infection",
        "term_diabetes": "Diabetes",
        "term_hypertension": "Hypertension",
        "term_coronary_heart_disease": "Coronary heart disease",
        "term_etiology_prefix": "Etiology: ",
        "adjustment_factors": "Age, sex, BMI, etiology, MELD-Na, complications (ascites, varices, HE, infection), and comorbidities (diabetes, hypertension, CHD)",
        "variance_standard": "Conventional model SE",
        "variance_cluster": "Cluster-robust SE by patient",
        "model_status_failed": "Model did not converge",
        "etiology_unclassified": "Unclassified",
        "etiology_mixed": "Mixed etiology",
        "etiology_viral": "Viral",
        "etiology_cholestatic": "Cholestatic",
        "etiology_autoimmune": "Autoimmune",
        "etiology_alcohol": "Alcoholic",
    },
}


def normalize_lang(lang: str | None) -> str:
    if lang and lang.lower() in SUPPORTED_LANGS:
        return lang.lower()
    return "zh"


def t(key: str, lang: str = "zh", **kwargs: object) -> str:
    locale = normalize_lang(lang)
    template = STRINGS[locale].get(key, STRINGS["zh"].get(key, key))
    return template.format(**kwargs) if kwargs else template


def etiology_label(raw: str, lang: str = "zh") -> str:
    mapping = {
        "未分类": "etiology_unclassified",
        "混合病因": "etiology_mixed",
        "病毒性": "etiology_viral",
        "胆汁淤积性": "etiology_cholestatic",
        "自身免疫性": "etiology_autoimmune",
        "酒精性": "etiology_alcohol",
    }
    key = mapping.get(raw)
    if key:
        return t(key, lang)
    return raw
