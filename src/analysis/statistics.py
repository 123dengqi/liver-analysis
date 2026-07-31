from __future__ import annotations

import math
import warnings

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

from src.i18n import etiology_label, t


def _p_text(value: float | None) -> str:
    if value is None or not np.isfinite(value):
        return "NA"
    return "<0.001" if value < 0.001 else f"{value:.3f}"


def _median_iqr(series: pd.Series) -> str:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return "NA"
    q1, median, q3 = values.quantile([0.25, 0.5, 0.75])
    return f"{median:.1f} ({q1:.1f}-{q3:.1f})"


def _n_percent(series: pd.Series, predicate=None) -> str:
    valid = series.dropna()
    if valid.empty:
        return "NA"
    selected = predicate(valid) if predicate else valid.astype(bool)
    count = int(selected.sum())
    return f"{count} ({100 * count / len(valid):.1f}%)"


def _continuous_p(df: pd.DataFrame, column: str, group: str) -> float:
    groups = [g[column].dropna() for _, g in df.groupby(group, observed=True)]
    if len(groups) != 2 or min(map(len, groups), default=0) == 0:
        return np.nan
    return float(stats.mannwhitneyu(groups[0], groups[1], alternative="two-sided").pvalue)


def _categorical_p(df: pd.DataFrame, column: str, group: str) -> float:
    table = pd.crosstab(df[column], df[group])
    if table.shape[0] < 2 or table.shape[1] < 2:
        return np.nan
    if table.shape == (2, 2) and (table.to_numpy() < 5).any():
        return float(stats.fisher_exact(table.to_numpy()).pvalue)
    return float(stats.chi2_contingency(table.to_numpy(), correction=False).pvalue)


def _variable_label(label_key: str, lang: str, polypharmacy_threshold: int, malnutrition_threshold: int) -> str:
    if label_key == "var_polypharmacy":
        return t(label_key, lang, threshold=polypharmacy_threshold)
    if label_key == "var_high_malnutrition_risk":
        return t(label_key, lang, threshold=malnutrition_threshold)
    return t(label_key, lang)


TABLE_VARIABLES = [
    ("var_age", "age", "continuous"),
    ("var_male", "sex", "male"),
    ("var_bmi", "bmi", "continuous"),
    ("var_medication_count", "medication_count", "continuous"),
    ("var_polypharmacy", "polypharmacy", "binary"),
    ("var_rfh_npt", "rfh_npt", "continuous"),
    ("var_high_malnutrition_risk", "high_malnutrition_risk", "binary"),
    ("var_meld_na", "meld_na", "continuous"),
    ("var_albumin", "albumin_g_l", "continuous"),
    ("var_hemoglobin", "hemoglobin", "continuous"),
    ("var_length_of_stay", "length_of_stay", "continuous"),
    ("var_etiology_viral", "etiology", "viral"),
    ("var_etiology_alcohol", "etiology", "alcohol"),
]


def comparison_table(
    df: pd.DataFrame,
    group: str,
    labels: tuple[str, str],
    lang: str = "zh",
    polypharmacy_threshold: int = 5,
    malnutrition_threshold: int = 2,
) -> list[dict]:
    result: list[dict] = []
    working = df[df[group].notna()].copy()
    working[group] = working[group].astype(bool)
    for label_key, column, kind in TABLE_VARIABLES:
        if column not in working:
            continue
        label = _variable_label(label_key, lang, polypharmacy_threshold, malnutrition_threshold)
        if kind == "continuous":
            overall = _median_iqr(working[column])
            values = [_median_iqr(working.loc[working[group] == flag, column]) for flag in (False, True)]
            p_value = _continuous_p(working[[column, group]].dropna(), column, group)
        else:
            if kind == "male":
                predicate = lambda s: s.eq("男")
            elif kind == "viral":
                predicate = lambda s: s.eq("病毒性")
            elif kind == "alcohol":
                predicate = lambda s: s.eq("酒精性")
            else:
                predicate = lambda s: s.astype(bool)
            overall = _n_percent(working[column], predicate)
            values = [_n_percent(working.loc[working[group] == flag, column], predicate) for flag in (False, True)]
            transformed = predicate(working[column]).astype(int)
            p_df = pd.DataFrame({"value": transformed, group: working[group]})
            p_value = _categorical_p(p_df, "value", group)
        result.append({
            "variable": label, "overall": overall,
            "group0": values[0], "group1": values[1],
            "group0_label": labels[0], "group1_label": labels[1],
            "p_value": _p_text(p_value),
        })
    return result


def age_group_summary(df: pd.DataFrame) -> dict:
    rows: list[dict] = []
    for label, group in df.groupby("age_group", observed=False):
        valid_outcome = group["high_malnutrition_risk"].dropna()
        rows.append({
            "age_group": str(label),
            "n": int(len(group)),
            "medication_median": round(float(group["medication_count"].median()), 2) if len(group) else None,
            "polypharmacy_pct": round(float(group["polypharmacy"].mean() * 100), 1) if len(group) else None,
            "malnutrition_pct": round(float(valid_outcome.astype(bool).mean() * 100), 1) if len(valid_outcome) else None,
        })
    group_codes = df["age_group"].cat.codes if hasattr(df["age_group"], "cat") else pd.Categorical(df["age_group"]).codes
    valid = group_codes >= 0
    med_p = stats.kruskal(*[g["medication_count"] for _, g in df.groupby("age_group", observed=True)]).pvalue
    poly_table = pd.crosstab(df["age_group"], df["polypharmacy"])
    mal_table = pd.crosstab(df["age_group"], df["high_malnutrition_risk"])
    poly_p = stats.chi2_contingency(poly_table, correction=False).pvalue if poly_table.shape[1] == 2 else np.nan
    mal_p = stats.chi2_contingency(mal_table, correction=False).pvalue if mal_table.shape[1] == 2 else np.nan
    return {"rows": rows, "p_values": {"medications": _p_text(med_p), "polypharmacy": _p_text(poly_p), "malnutrition": _p_text(mal_p)}}


def _fit_logistic(data: pd.DataFrame, columns: list[str], cluster_column: str | None = None) -> tuple[object | None, pd.DataFrame]:
    selected = ["high_malnutrition_risk", *columns]
    if cluster_column:
        selected.append(cluster_column)
    model_data = data[selected].dropna().copy()
    clusters = model_data.pop(cluster_column) if cluster_column else None
    y = model_data.pop("high_malnutrition_risk").astype(int)
    x = pd.get_dummies(model_data, columns=[c for c in columns if c == "etiology"], drop_first=True, dtype=float)
    x = x.astype(float)
    x = sm.add_constant(x, has_constant="add")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fit_kwargs = {"disp": False, "maxiter": 200}
            if clusters is not None:
                fit_kwargs.update({"cov_type": "cluster", "cov_kwds": {"groups": clusters}})
            fitted = sm.Logit(y, x).fit(**fit_kwargs)
        return fitted, x
    except Exception:
        return None, x


def logistic_results(
    df: pd.DataFrame,
    cluster_by_patient: bool = False,
    lang: str = "zh",
    polypharmacy_threshold: int = 5,
) -> dict:
    data = df.copy()
    data["sex_male"] = data["sex"].eq("男").astype(float)
    cluster_column = "patient_id" if cluster_by_patient else None
    unadjusted, un_x = _fit_logistic(data, ["polypharmacy"], cluster_column)
    adjusted_columns = ["polypharmacy", "age", "sex_male", "bmi", "etiology", "meld_na"]
    adjusted, adj_x = _fit_logistic(data, adjusted_columns, cluster_column)

    def rows_for(model, x, model_name_key: str) -> list[dict]:
        if model is None:
            return []
        term_keys = {
            "polypharmacy": "term_polypharmacy",
            "age": "term_age",
            "sex_male": "term_sex_male",
            "bmi": "term_bmi",
            "meld_na": "term_meld_na",
        }
        rows = []
        ci = model.conf_int()
        for term in model.params.index:
            if term == "const":
                continue
            if term in term_keys:
                label = t(term_keys[term], lang, threshold=polypharmacy_threshold)
            elif term.startswith("etiology_"):
                raw = term.replace("etiology_", "")
                label = t("term_etiology_prefix", lang) + etiology_label(raw, lang)
            else:
                label = term
            rows.append({
                "model": t(model_name_key, lang),
                "term": label,
                "term_key": term if term != "const" else None,
                "or": round(float(math.exp(model.params[term])), 3),
                "ci_low": round(float(math.exp(ci.loc[term, 0])), 3),
                "ci_high": round(float(math.exp(ci.loc[term, 1])), 3),
                "p_value": _p_text(float(model.pvalues[term])),
                "n": int(model.nobs),
            })
        return rows

    return {
        "unadjusted": rows_for(unadjusted, un_x, "model_unadjusted"),
        "adjusted": rows_for(adjusted, adj_x, "model_adjusted"),
        "adjusted_n": int(adjusted.nobs) if adjusted is not None else 0,
        "adjustment": t("adjustment_factors", lang),
        "variance_estimator": t("variance_cluster", lang) if cluster_by_patient else t("variance_standard", lang),
        "status": "ok" if adjusted is not None else t("model_status_failed", lang),
    }


def summary_metrics(df: pd.DataFrame) -> dict:
    outcome = df["high_malnutrition_risk"].dropna().astype(bool)
    exposed = df["polypharmacy"].astype(bool)
    return {
        "n": int(len(df)),
        "unique_patients": int(df["patient_id"].nunique()),
        "polypharmacy_n": int(exposed.sum()),
        "polypharmacy_pct": round(float(exposed.mean() * 100), 1),
        "malnutrition_n": int(outcome.sum()),
        "malnutrition_pct": round(float(outcome.mean() * 100), 1),
        "medication_median": round(float(df["medication_count"].median()), 1),
        "meld_na_median": round(float(df["meld_na"].median()), 1),
        "complete_case_n": int(df[["high_malnutrition_risk", "polypharmacy", "age", "sex", "bmi", "etiology", "meld_na"]].dropna().shape[0]),
    }
