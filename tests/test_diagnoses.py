from src.data.diagnoses import (
    coded_binary,
    has_coronary_heart_disease,
    has_diabetes,
    has_hypertension,
    resolve_binary,
)


def test_hypertension_excludes_portal_hypertension():
    assert has_hypertension("肝硬化，门脉高压，脾大") is False
    assert has_hypertension("门静脉高压，肺动脉高压") is False
    assert has_hypertension("高血压3级，门脉高压性胃肠病") is True


def test_diabetes_from_diagnosis():
    assert has_diabetes("2型糖尿病，高血压3级") is True
    assert has_diabetes("肝硬化失代偿期，腹水") is False


def test_chd_patterns_and_exclusions():
    assert has_coronary_heart_disease("冠状动脉粥样硬化性心脏病，高血压") is True
    assert has_coronary_heart_disease("冠状动脉支架植入后状态") is True
    assert has_coronary_heart_disease("陈旧性心肌梗死") is True
    assert has_coronary_heart_disease("冠状动脉肌桥") is False
    assert has_coronary_heart_disease("肝硬化，腹水") is False


def test_coded_binary_handles_uncertain_yes():
    assert coded_binary("1？") is True
    assert coded_binary("？") is None
    assert resolve_binary("？", "肝硬化伴食管胃底静脉曲张", lambda text: "静脉曲张" in str(text)) is True
