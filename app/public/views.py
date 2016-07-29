from app import app
from flask import render_template, jsonify, json


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.route("/terms_and_conditions")
def terms_and_conditions():
    try:
        data = json.load(
            open("app/static/text/terms_and_conditions.json", "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@app.route("/test_reports")
def tests_reports():
    from app.report.reports_generation import monthly_reports_generation

    monthly_reports_generation()
    return "Reportes generados", 200
