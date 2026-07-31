from __future__ import annotations

from flask import Flask, jsonify, render_template, request, send_from_directory

from src.config import CONFIG
from src.i18n import normalize_lang
from src.services.dashboard import DashboardService


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    service = DashboardService(CONFIG)
    service.export_outputs()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/dashboard")
    def dashboard():
        strategy = request.args.get("strategy", CONFIG.default_strategy)
        lang = normalize_lang(request.args.get("lang"))
        if strategy not in {"first", "latest", "all"}:
            return jsonify({"error": "strategy must be first, latest, or all"}), 400
        return jsonify(service.build(strategy, lang=lang))

    @app.get("/downloads/<path:filename>")
    def downloads(filename: str):
        allowed = {
            "analysis_cohort_anonymized.csv", "medication_manual_review.csv",
            "table_polypharmacy.csv", "table_malnutrition.csv", "logistic_regression.csv",
        }
        if filename not in allowed:
            return jsonify({"error": "file not available"}), 404
        return send_from_directory(CONFIG.output_dir, filename, as_attachment=True)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

