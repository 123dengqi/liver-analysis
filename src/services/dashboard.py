from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.analysis.statistics import age_group_summary, comparison_table, logistic_results, summary_metrics
from src.config import AnalysisConfig
from src.data.cohort import enrich_registry, select_analysis_cohort
from src.data.loader import load_registry


class DashboardService:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.raw = load_registry(config.data_file, config.sheet_name)
        self.enriched = enrich_registry(self.raw, config)
        self._cache: dict[str, dict] = {}

    def build(self, strategy: str = "first") -> dict:
        if strategy in self._cache:
            return self._cache[strategy]
        cohort = select_analysis_cohort(self.enriched, strategy, self.config)
        payload = {
            "meta": {
                "strategy": strategy,
                "strategies": {"first": "首次住院记录", "latest": "末次住院记录", "all": "全部住院记录"},
                "polypharmacy_definition": f"出院药物种类≥{self.config.polypharmacy_threshold}",
                "malnutrition_definition": f"RFH-NPT≥{self.config.malnutrition_threshold}",
                "severity_measure": "MELD-Na评分",
                "analysis_unit_note": "首次/末次策略每位患者仅保留一条记录；全部记录仅用于敏感性分析。",
            },
            "summary": summary_metrics(cohort),
            "age_groups": age_group_summary(cohort),
            "polypharmacy_table": comparison_table(cohort, "polypharmacy", ("非多重用药", "多重用药")),
            "malnutrition_table": comparison_table(cohort, "high_malnutrition_risk", ("低风险", "高风险")),
            "logistic": logistic_results(cohort, cluster_by_patient=(strategy == "all")),
            "quality": self.quality_summary(cohort),
        }
        self._cache[strategy] = payload
        return payload

    def quality_summary(self, cohort: pd.DataFrame) -> dict:
        confidence = cohort["medication_parse_confidence"].value_counts().to_dict()
        formula_checked = cohort["meld_na_formula_match"].notna().sum() if "meld_na_formula_match" in cohort else 0
        formula_mismatch = int((cohort["meld_na_formula_match"] == False).sum()) if "meld_na_formula_match" in cohort else 0
        return {
            "source_records": int(len(self.enriched)),
            "source_patients": int(self.enriched["patient_id"].nunique()),
            "excluded_age_ineligible": int((~self.enriched["is_adult"]).sum()),
            "under_18": int(self.enriched["age"].lt(self.config.adult_age).sum()),
            "missing_age": int(self.enriched["age"].isna().sum()),
            "missing_rfh_npt": int(self.enriched["rfh_npt"].isna().sum()),
            "missing_meld_na": int(cohort["meld_na"].isna().sum()),
            "missing_bmi": int(cohort["bmi"].isna().sum()),
            "duplicate_records_removed": int(len(self.enriched[self.enriched["is_adult"] & self.enriched["rfh_npt"].notna()]) - len(cohort)),
            "medication_parse_confidence": {str(k): int(v) for k, v in confidence.items()},
            "manual_review_n": int(cohort["medication_parse_confidence"].ne("high").sum()),
            "meld_na_formula_checked": int(formula_checked),
            "meld_na_formula_mismatch": formula_mismatch,
        }

    def export_outputs(self) -> None:
        output_dir = self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        for strategy in ("first", "latest", "all"):
            payload = self.build(strategy)
            with (output_dir / f"dashboard_{strategy}.json").open("w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)

        cohort = select_analysis_cohort(self.enriched, "first", self.config)
        anonymous_columns = [
            "patient_id", "source_row", "sex", "age", "bmi", "rfh_npt",
            "high_malnutrition_risk", "medication_count", "polypharmacy", "medication_names",
            "medication_parse_confidence", "medication_review_reason", "etiology", "meld",
            "meld_na", "albumin_g_l", "hemoglobin", "length_of_stay", "admission_date",
        ]
        cohort[anonymous_columns].to_csv(output_dir / "analysis_cohort_anonymized.csv", index=False, encoding="utf-8-sig")
        review_columns = [
            "patient_id", "source_row", "discharge_medications", "medication_count",
            "medication_names", "medication_parse_confidence", "medication_review_reason",
        ]
        cohort.loc[cohort["medication_parse_confidence"].ne("high"), review_columns].to_csv(
            output_dir / "medication_manual_review.csv", index=False, encoding="utf-8-sig"
        )
        pd.DataFrame(self.build("first")["polypharmacy_table"]).to_csv(
            output_dir / "table_polypharmacy.csv", index=False, encoding="utf-8-sig"
        )
        pd.DataFrame(self.build("first")["malnutrition_table"]).to_csv(
            output_dir / "table_malnutrition.csv", index=False, encoding="utf-8-sig"
        )
        logistic = self.build("first")["logistic"]
        pd.DataFrame(logistic["unadjusted"] + logistic["adjusted"]).to_csv(
            output_dir / "logistic_regression.csv", index=False, encoding="utf-8-sig"
        )
        primary = next(
            (row for row in logistic["adjusted"] if row["term"].startswith("多重用药")),
            None,
        )
        unadjusted = logistic["unadjusted"][0] if logistic["unadjusted"] else None
        summary = self.build("first")["summary"]
        report_lines = [
            "# 主分析摘要",
            "",
            "分析单元：每位成人患者首次有 RFH-NPT 记录的住院。",
            "",
            f"- 纳入患者：{summary['n']}例。",
            f"- 多重用药（出院药物≥{self.config.polypharmacy_threshold}种）：{summary['polypharmacy_n']}例（{summary['polypharmacy_pct']}%）。",
            f"- 高营养不良风险（RFH-NPT≥{self.config.malnutrition_threshold}）：{summary['malnutrition_n']}例（{summary['malnutrition_pct']}%）。",
            f"- 多变量完整病例：{summary['complete_case_n']}例。",
        ]
        if unadjusted:
            report_lines.append(
                f"- 未调整关联：OR={unadjusted['or']}，95%CI {unadjusted['ci_low']}-{unadjusted['ci_high']}，P={unadjusted['p_value']}。"
            )
        if primary:
            report_lines.append(
                f"- 调整年龄、性别、BMI、病因和MELD-Na后：OR={primary['or']}，95%CI {primary['ci_low']}-{primary['ci_high']}，P={primary['p_value']}。"
            )
        report_lines.extend([
            "",
            "主分析中未调整关联有统计学意义，但多变量校正后未达到P<0.05，不能表述为独立危险因素。末次记录和全部记录口径仅作为敏感性分析。",
            "",
            "本分析为观察性研究，结果表示关联而非因果。药物自由文本的中低置信度记录应在论文定稿前人工复核。",
        ])
        (output_dir / "主分析摘要.md").write_text("\n".join(report_lines), encoding="utf-8")
