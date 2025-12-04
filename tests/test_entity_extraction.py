from src.services.ner_service import NERService


def test_company_extraction():
    ner = NERService()
    text = "HDFC Bank announces 15% dividend, board approves stock buyback"
    ents = ner.extract(text)
    assert any(e["type"] == "COMPANY" and "HDFC Bank" in e["name"] for e in ents)


def test_regulator_extraction():
    ner = NERService()
    text = "RBI raises repo rate by 25bps"
    ents = ner.extract(text)
    assert any(e["type"] == "REGULATOR" and (e["name"].lower() == "rbi" or e.get("normalized") == "rbi") for e in ents)


def test_sector_tagging():
    ner = NERService()
    text = "Banking sector NPAs decline to 5-year low"
    ents = ner.extract(text)
    assert any(e["type"] == "SECTOR" and e["name"].lower().startswith("banking") for e in ents)


def test_entity_precision_benchmark():
    ner = NERService()
    samples = [
        ("HDFC Bank announces dividend", {("COMPANY", "hdfc bank")} ),
        ("RBI announces policy measures", {("REGULATOR", "rbi")} ),
        ("Banking sector update", {("SECTOR", "banking")} ),
    ]
    correct = 0
    total = len(samples)
    for text, expected in samples:
        ents = ner.extract(text)
        got = {(e["type"], (e.get("normalized") or e["name"]).lower()) for e in ents}
        if any(exp in got for exp in expected):
            correct += 1
    precision = correct / total
    assert precision >= 0.9
