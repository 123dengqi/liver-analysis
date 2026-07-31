from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AnalysisConfig:
    data_file: Path = ROOT / "2022.10.14.营养评分数据统计.xlsx"
    sheet_name: str = "汇总表"
    polypharmacy_threshold: int = 5
    malnutrition_threshold: int = 2
    adult_age: int = 18
    default_strategy: str = "all"
    output_dir: Path = ROOT / "outputs"


CONFIG = AnalysisConfig()

