from app import application
from app.public.views import page_not_found
from flask import json, jsonify


@application.route("/reports/general_reports/<year>/<month>")
def general_reports(year, month):
    try:
        data = json.load(
            open("app/static/reports/general_reports/" + year + "/general_report_" + month + "_" + year + ".json",
                 "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@application.route("/reports/network_reports/<year>/<month>")
def network_reports(year, month):
    try:
        data = json.load(
            open("app/static/reports/network_reports/" + year + "/network_report_" + month + "_" + year + ".json",
                 "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@application.route("/reports/signal_reports/<year>/<month>")
def signal_reports(year, month):
    try:
        data = json.load(
            open("app/static/reports/signal_reports/" + year + "/signal_report_" + month + "_" + year + ".json",
                 "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@application.route("/reports/apps_reports/<year>/<month>")
def apps_reports(year, month):
    try:
        data = json.load(
            open("app/static/reports/apps_reports/" + year + "/apps_report_" + month + "_" + year + ".json",
                 "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)