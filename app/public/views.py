from flask import render_template, json, jsonify, redirect

from app import app


@app.route("/")
def index():
    return redirect("http://www.adkintunmobile.cl", code=302)


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


# Trigger for reports generation
@app.route("/generate_reports")
def generate_reports():
    from app.report.reports_generation import monthly_reports_generation

    monthly_reports_generation()
    return "Reports Generated", 200


# Trigger for reports generation
@app.route("/geolocalizate_antennas")
def geolocalizate_antennas():
    from app.data.antennas_geolocalization import update_antennas_localization

    geolocalizated_antennas = update_antennas_localization(max_number_of_queries=1000)
    return "Geolocalizated antennas:" + str(geolocalizated_antennas), 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
