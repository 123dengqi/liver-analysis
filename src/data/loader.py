from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


COLUMN_MAP = {
    "姓名": "patient_name",
    "性别": "sex",
    "年龄": "age",
    "身高（m)": "height_m",
    "体重（Kg）": "weight_kg",
    "BMI": "bmi",
    "RFH-NPT评分": "rfh_npt",
    "评分日期": "assessment_date",
    "入院时间": "admission_date",
    "出院时间": "discharge_date",
    "死亡时间": "death_date",
    "住院次数": "admission_count",
    "住院天数": "length_of_stay",
    "出院诊断": "diagnosis",
    "病毒": "etiology_viral",
    "酒精": "etiology_alcohol",
    "免疫": "etiology_autoimmune",
    "PBC/PSC/重叠": "etiology_cholestatic",
    "其他": "etiology_other",
    "腹水": "ascites_coded",
    "肝脑": "hepatic_encephalopathy_coded",
    "食管胃底静脉曲张": "varices_coded",
    "感染": "infection",
    "门脉高压": "portal_hypertension",
    "CTP评分": "ctp_score",
    "MELD评分": "meld",
    "MELD Na": "meld_na",
    "Na": "meld_na_sodium_clipped",
    "Na.1": "sodium",
    "WBC": "wbc",
    "Hb": "hemoglobin",
    "白蛋白（g/L）": "albumin_g_l",
    "出院带药": "discharge_medications",
}

NUMERIC_COLUMNS = {
    "age", "height_m", "weight_kg", "bmi", "rfh_npt", "admission_count",
    "length_of_stay", "ctp_score", "meld", "meld_na", "wbc", "hemoglobin",
    "albumin_g_l", "meld_na_sodium_clipped", "sodium", "etiology_viral", "etiology_alcohol", "etiology_autoimmune",
    "etiology_cholestatic", "etiology_other", "infection", "portal_hypertension",
}

DATE_COLUMNS = {"assessment_date", "admission_date", "discharge_date", "death_date"}


def _deduplicate_columns(columns: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    result: list[str] = []
    for column in columns:
        count = seen.get(column, 0)
        result.append(column if count == 0 else f"{column}.{count}")
        seen[column] = count + 1
    return result


def load_registry(path: Path, sheet_name: str = "汇总表") -> pd.DataFrame:
    """Load the registry whose second Excel row contains the actual field names."""
    raw = pd.read_excel(path, sheet_name=sheet_name, header=1)
    raw.columns = _deduplicate_columns([str(c).strip() for c in raw.columns])

    selected: dict[str, pd.Series] = {}
    for source, target in COLUMN_MAP.items():
        if source in raw.columns:
            selected[target] = raw[source]
    df = pd.DataFrame(selected)

    df = df[df["patient_name"].notna()].copy()
    df["patient_name"] = df["patient_name"].astype(str).str.strip()
    df = df[df["patient_name"].ne("")].copy()

    for column in NUMERIC_COLUMNS.intersection(df.columns):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in DATE_COLUMNS.intersection(df.columns):
        df[column] = pd.to_datetime(df[column], errors="coerce")

    df["sex"] = df["sex"].replace({1: "男", 2: "女", "1": "男", "2": "女"})
    df.loc[~df["sex"].isin(["男", "女"]), "sex"] = np.nan
    df["source_row"] = df.index + 3
    return df.reset_index(drop=True)
