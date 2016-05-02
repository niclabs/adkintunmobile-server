from datetime import datetime

from flask import render_template, request

from app import app


def get_min_date(dateStr, format):
    try:
        return datetime.strptime(dateStr, format).date()
    except Exception:
        pass


def get_max_date(dateStr, format):
    try:
        return datetime.strptime(dateStr, format).date()
    except Exception:
        pass


@app.route('/report/')
def report_index():
    return render_template('report/login.html')


@app.route('/report/totales')
def total_devices_reported():
    from app.report.report import total_devices_reported
    from app.report.report import total_sims_registered
    from app.report.report import total_gsm_events

    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    total_devices = total_devices_reported(min_date, max_date)
    total_sims = total_sims_registered(min_date, max_date)
    total_events = total_gsm_events(min_date, max_date)
    return render_template('report/totales.html', total_devices=total_devices, total_sims=total_sims,
                           total_events=total_events, min_date=min_date, max_date=max_date)


@app.route('/report/total_device_for_carrier')
def device_for_carrier():
    from app.report.report import total_device_for_carrier

    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    carriers = total_device_for_carrier(min_date, max_date)
    return render_template('report/device_for_carrier.html', carriers=carriers,
                           min_date=min_date, max_date=max_date)


@app.route('/report/total_sims_for_carrier')
def sims_for_carrier():
    from app.report.report import total_sims_for_carrier

    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    carriers = total_sims_for_carrier(min_date, max_date)
    return render_template('report/sims_for_carrier.html', carriers=carriers,
                           min_date=min_date, max_date=max_date)


@app.route('/report/total_events_for_carrier')
def events_for_carrier():
    from app.report.report import total_events_for_carrier

    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    carriers = total_events_for_carrier(min_date, max_date)
    return render_template('report/events_for_carrier.html', carriers=carriers,
                           min_date=min_date, max_date=max_date)
