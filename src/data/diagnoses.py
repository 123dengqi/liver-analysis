from __future__ import annotations

import pandas as pd


_YES = {1, 1.0, "1", "1.0", "1？", "是", True}
_NO = {0, 0.0, "0", "0.0", "否", False}

_HYPERTENSION_EXCLUDE = ("门静脉高压", "门脉高压", "肺动脉高压")

_CHD_PATTERNS = (
    "冠心病",
    "冠状动脉性心脏病",
    "冠状动脉粥样硬化性心脏病",
    "冠状动脉心脏病",
    "冠状动脉粥样硬化",
    "冠状动脉支架",
    "冠脉支架",
    "冠状动脉搭桥",
    "冠脉搭桥",
    "心肌梗死",
    "心梗",
    "心绞痛",
    "缺血性心肌病",
    "冠状动脉缺血",
)

_CHD_EXCLUDE = ("冠状动脉肌桥", "冠脉肌桥")


def _text(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def coded_binary(value: object) -> bool | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, str):
        text = value.strip()
        if text in _YES:
            return True
        if text in _NO:
            return False
        return None
    if value in _YES:
        return True
    if value in _NO:
        return False
    return None


def has_ascites(diagnosis: object) -> bool:
    text = _text(diagnosis)
    return "腹水" in text or "腹腔积液" in text


def has_varices(diagnosis: object) -> bool:
    return "静脉曲张" in _text(diagnosis)


def has_hepatic_encephalopathy(diagnosis: object) -> bool:
    text = _text(diagnosis)
    return "肝性脑病" in text or "肝性昏迷" in text


def has_infection(diagnosis: object) -> bool:
    text = _text(diagnosis)
    return any(token in text for token in ("感染", "肺炎", "腹膜炎", "败血症", "脓毒"))


def has_diabetes(diagnosis: object) -> bool:
    return "糖尿病" in _text(diagnosis)


def has_hypertension(diagnosis: object) -> bool:
    text = _text(diagnosis)
    for phrase in _HYPERTENSION_EXCLUDE:
        text = text.replace(phrase, "")
    return "高血压" in text


def has_coronary_heart_disease(diagnosis: object) -> bool:
    text = _text(diagnosis)
    if any(token in text for token in _CHD_EXCLUDE) and not any(token in text for token in _CHD_PATTERNS):
        return False
    cleaned = text
    for token in _CHD_EXCLUDE:
        cleaned = cleaned.replace(token, "")
    return any(token in cleaned for token in _CHD_PATTERNS)


def resolve_binary(coded: object, diagnosis: object, parser) -> bool:
    flag = coded_binary(coded)
    if flag is not None:
        return flag
    return bool(parser(diagnosis))


def extract_clinical_flags(row: pd.Series) -> dict[str, object]:
    diagnosis = row.get("diagnosis")
    ascites = resolve_binary(row.get("ascites_coded"), diagnosis, has_ascites)
    varices = resolve_binary(row.get("varices_coded"), diagnosis, has_varices)
    encephalopathy = resolve_binary(row.get("hepatic_encephalopathy_coded"), diagnosis, has_hepatic_encephalopathy)
    infection = resolve_binary(row.get("infection"), diagnosis, has_infection)
    diabetes = has_diabetes(diagnosis)
    hypertension = has_hypertension(diagnosis)
    chd = has_coronary_heart_disease(diagnosis)
    evidence = []
    if diabetes:
        evidence.append("糖尿病")
    if hypertension:
        evidence.append("高血压")
    if chd:
        matches = [token for token in _CHD_PATTERNS if token in _text(diagnosis)]
        evidence.append("冠心病:" + "/".join(matches[:3]) if matches else "冠心病")
    return {
        "ascites": ascites,
        "varices": varices,
        "hepatic_encephalopathy": encephalopathy,
        "infection": infection,
        "diabetes": diabetes,
        "hypertension": hypertension,
        "coronary_heart_disease": chd,
        "comorbidity_evidence": "；".join(evidence),
    }
