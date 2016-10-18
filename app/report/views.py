from flask import json, jsonify

from app import application
from app import autoindex
from app.public.views import page_not_found


# listing reports folder
# NOT AUTHORIZATION REQUIRED

@application.route("/reports/")
@application.route("/reports/<path:path>")
def reports(path=""):
    return autoindex.render_autoindex(path=path, endpoint="reports", mimetype="application/json")


# reports urls for frontend

@application.route("/general_report/<year>/<month>/")
def general_report(year, month):
    return api_reports(type="general_report", year=year, month=month)


@application.route("/apps_report/<year>/<month>/")
def apps_report(year, month):
    return api_reports(type="apps_report", year=year, month=month)


@application.route("/network_report/<year>/<month>/")
def network_report(year, month):
    return api_reports(type="network_report", year=year, month=month)


@application.route("/signal_report/<year>/<month>/")
def signal_report(year, month):
    return api_reports(type="signal_report", year=year, month=month)


# utils


def api_reports(type, year, month):
    try:
        data = json.load(
            open("app/static/reports/" + year + "/" + month + "/" + type + "_" + month + "_" + year + ".json",
                 "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)
