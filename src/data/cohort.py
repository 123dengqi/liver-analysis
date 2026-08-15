from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from src.config import AnalysisConfig
from src.data.diagnoses import extract_clinical_flags
from src.data.medications import parse_medications


def _primary_etiology(row: pd.Series) -> str:
    flags = [
        ("病毒性", row.get("etiology_viral")),
        ("酒精性", row.get("etiology_alcohol")),
        ("自身免疫性", row.get("etiology_autoimmune")),
        ("胆汁淤积性", row.get("etiology_cholestatic")),
        ("其他", row.get("etiology_other")),
    ]
    active = [label for label, value in flags if pd.notna(value) and value == 1]
    if len(active) == 1:
        return active[0]
    if len(active) > 1:
        return "混合病因"
    return "未分类"


def _patient_id(name: str) -> str:
    return "P-" + hashlib.sha256(name.encode("utf-8")).hexdigest()[:8].upper()


def enrich_registry(df: pd.DataFrame, config: AnalysisConfig) -> pd.DataFrame:
    enriched = df.copy()
    parsed = enriched["discharge_medications"].apply(parse_medications)
    enriched["medication_count"] = parsed.map(lambda x: x.count)
    enriched["medication_names"] = parsed.map(lambda x: " | ".join(x.names))
    enriched["medication_parse_confidence"] = parsed.map(lambda x: x.confidence)
    enriched["medication_review_reason"] = parsed.map(lambda x: x.review_reason)
    enriched["polypharmacy"] = enriched["medication_count"] >= config.polypharmacy_threshold
    enriched["high_malnutrition_risk"] = (enriched["rfh_npt"] >= config.malnutrition_threshold).astype("boolean")
    enriched.loc[enriched["rfh_npt"].isna(), "high_malnutrition_risk"] = pd.NA
    enriched["etiology"] = enriched.apply(_primary_etiology, axis=1)
    flags = enriched.apply(extract_clinical_flags, axis=1, result_type="expand")
    for column in flags.columns:
        enriched[column] = flags[column]
    enriched["patient_id"] = enriched["patient_name"].map(_patient_id)
    enriched["age_group"] = pd.cut(
        enriched["age"], bins=[0, 49, 59, 69, np.inf],
        labels=["<50", "50-59", "60-69", "≥70"], right=True,
    )
    enriched["is_adult"] = enriched["age"].ge(config.adult_age)
    enriched["meld_na_valid"] = enriched["meld_na"].between(0, 60, inclusive="both")
    if {"meld", "meld_na", "meld_na_sodium_clipped"}.issubset(enriched.columns):
        enriched["meld_na_recalculated"] = enriched["meld"] + 1.59 * (135 - enriched["meld_na_sodium_clipped"])
        enriched["meld_na_formula_match"] = (
            enriched["meld_na"] - enriched["meld_na_recalculated"]
        ).abs().le(0.02).astype("boolean")
        missing = enriched[["meld", "meld_na", "meld_na_sodium_clipped"]].isna().any(axis=1)
        enriched.loc[missing, "meld_na_formula_match"] = pd.NA
    return enriched


def select_analysis_cohort(df: pd.DataFrame, strategy: str, config: AnalysisConfig) -> pd.DataFrame:
    eligible = df[df["is_adult"] & df["rfh_npt"].notna()].copy()
    eligible = eligible.sort_values(["patient_name", "admission_date", "source_row"], na_position="last")
    if strategy == "first":
        eligible = eligible.drop_duplicates("patient_name", keep="first")
    elif strategy == "latest":
        eligible = eligible.drop_duplicates("patient_name", keep="last")
    elif strategy != "all":
        raise ValueError(f"Unsupported cohort strategy: {strategy}")
    return eligible.reset_index(drop=True)
