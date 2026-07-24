from src.app import create_app


def test_dashboard_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/dashboard?strategy=first")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["summary"]["n"] > 0
    assert payload["meta"]["polypharmacy_definition"] == "出院药物种类≥5"
    assert payload["meta"]["malnutrition_definition"] == "RFH-NPT≥2"


def test_invalid_strategy():
    app = create_app()
    response = app.test_client().get("/api/dashboard?strategy=bad")
    assert response.status_code == 400


def test_frontend_contains_interaction_controls():
    app = create_app()
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    for marker in ("table-search", "strategy-feedback", "retry", "aria-selected", "skip-link"):
        assert marker in html
