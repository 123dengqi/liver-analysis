from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd


EMPTY_MARKERS = {"", "无", "无。", "无带药", "无出院带药", "未带药", "nan", "none", "/"}
SEPARATOR_RE = re.compile(r"[，,、；;\n]+")
LEADING_MARK_RE = re.compile(r"^[\s\d①②③④⑤⑥⑦⑧⑨⑩]+")
MANUFACTURER_RE = re.compile(r"^[（(][^）)]{1,8}[）)]")
DOSE_START_RE = re.compile(
    r"(?<![-(])(?=\d+(?:\.\d+)?\s*(?:mg|g|ml|mL|u|U|μg|ug|片|粒|丸|袋|支|滴|喷|揿|单位))",
    flags=re.IGNORECASE,
)
ROUTE_RE = re.compile(r"(?:口服|皮下|外用|静滴|静脉|餐前|餐后|睡前|嚼服|自备).*$", re.IGNORECASE)
DOSE_EVIDENCE_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:mg|g|ml|mL|u|U|μg|ug|片|粒|丸|袋|支|滴|喷|揿|单位)|(?:QD|BID|TID|QID|QN|QOD)",
    flags=re.IGNORECASE,
)
FORMULATION_RE = re.compile(r"(?:片|胶囊|颗粒|液|针|丸|散|凝胶|滴眼|喷雾|胰岛素|乳膏|栓|乳剂|合剂|口服溶液)")
DIRECTIVE_RE = re.compile(r"(?:无出院带药|嘱|继续|停用|必要时|调整|治疗|复查|医嘱|根据尿量)")


@dataclass(frozen=True)
class MedicationParse:
    count: int
    names: list[str]
    confidence: str
    review_reason: str


def _clean_fragment(fragment: str) -> str:
    value = fragment.strip(" 。.：:")
    value = LEADING_MARK_RE.sub("", value)
    while MANUFACTURER_RE.match(value):
        value = MANUFACTURER_RE.sub("", value, count=1).strip()
    return value


def _extract_name(fragment: str) -> str:
    value = _clean_fragment(fragment)
    value = re.sub(r"[（(]自备[）)]", "", value)
    value = DOSE_START_RE.split(value, maxsplit=1)[0]
    value = ROUTE_RE.sub("", value)
    value = re.sub(r"[（(][^）)]*(?:自备|白备)[^）)]*[）)]", "", value)
    return value.strip(" 。.：:")


def parse_medications(raw: object) -> MedicationParse:
    if pd.isna(raw):
        return MedicationParse(0, [], "low", "缺少出院带药记录")
    text = str(raw).strip()
    if text.lower() in EMPTY_MARKERS:
        return MedicationParse(0, [], "high", "")

    fragments = [_clean_fragment(part) for part in SEPARATOR_RE.split(text)]
    fragments = [part for part in fragments if part and part.lower() not in EMPTY_MARKERS]
    names: list[str] = []
    ambiguous: list[str] = []
    uncertain: list[str] = []
    for fragment in fragments:
        if DIRECTIVE_RE.search(fragment):
            ambiguous.append(fragment)
            continue
        name = _extract_name(fragment)
        if not name:
            ambiguous.append(fragment)
            continue
        if len(name) > 28 or re.search(r"(?:继续|停用|必要时|调整|治疗|复查|医嘱)", name):
            ambiguous.append(fragment)
        names.append(name)
        if not FORMULATION_RE.search(name) and not DOSE_EVIDENCE_RE.search(fragment):
            uncertain.append(fragment)

    unique_names = list(dict.fromkeys(names))
    if ambiguous:
        return MedicationParse(len(unique_names), unique_names, "low", "存在需人工确认的文本片段")
    if uncertain:
        return MedicationParse(len(unique_names), unique_names, "medium", "部分药名缺少常见剂型词")
    return MedicationParse(len(unique_names), unique_names, "high", "")
