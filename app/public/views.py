from flask import render_template, json, jsonify

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reports/general_reports/<year>/<month>')
def general_reports(year, month):
    try:
        data = json.load(
            open('app/static/reports/general_reports/' + year + '/general_report_' + month + '_' + year + '.json',
                 'r'))
        return jsonify(data)
    except Exception as e:
        return page_not_found(e)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
