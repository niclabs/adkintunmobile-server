from flask import render_template, json, jsonify, redirect

from app import application


@application.route("/")
def index():
    return redirect("http://www.adkintunmobile.cl", code=302)


@application.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@application.route("/terms_and_conditions")
def terms_and_conditions():
    try:
        data = json.load(
            open("app/static/text/terms_and_conditions.json", "r"))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
