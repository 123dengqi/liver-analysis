from src.data.medications import parse_medications


def test_empty_medications():
    assert parse_medications("无").count == 0


def test_chinese_delimiters_and_manufacturer_marks():
    parsed = parse_medications("(国)恩替卡韦分散片0.5mg口服QD，熊去氧胆酸胶囊250mg口服TID、乳果糖10ml口服TID")
    assert parsed.count == 3
    assert parsed.names == ["恩替卡韦分散片", "熊去氧胆酸胶囊", "乳果糖"]


def test_duplicates_are_counted_once():
    parsed = parse_medications("乳果糖10ml口服TID，乳果糖15ml口服QD")
    assert parsed.count == 1

