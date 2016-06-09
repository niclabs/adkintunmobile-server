from datetime import datetime

from app import app, db
from app.models.carrier import Carrier
from app.report.report_generation import total_devices_reported, total_sims_registered, total_gsm_events, \
    total_device_for_carrier, total_sims_for_carrier, total_gsm_events_for_carrier
from app.report.retrieve_processed_data import get_stored_data
from config import Visualization
from flask import render_template, request

real_time_visualization = Visualization.real_time_info


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
    from app.report.report_generation import generate_report
    generate_report()
    return render_template('report/index.html')


@app.route('/report/totales')
def total_devices_reported():
    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    if real_time_visualization:

        total_devices = total_devices_reported(min_date, max_date)
        total_sims = total_sims_registered(min_date, max_date)
        total_events = total_gsm_events(min_date, max_date)

    else:
        stored_data = get_stored_data(min_date, max_date)

        total_devices = stored_data.total_devices
        total_sims = stored_data.total_sims
        total_events = stored_data.total_events

    return render_template('report/totales.html', total_devices=total_devices, total_sims=total_sims,
                           total_events=total_events, min_date=min_date, max_date=max_date)


@app.route('/report/total_device_for_carrier')
def device_for_carrier():
    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    if real_time_visualization:

        carriers = total_device_for_carrier(min_date, max_date)

    else:
        stored_data = get_stored_data(min_date, max_date)
        carriers = db.session.query(Carrier).all()
        for carrier in carriers:
            carrier.devices_count = stored_data['devices_' + Carrier.carriers[carrier.name]]

    return render_template('report/device_for_carrier.html', carriers=carriers,
                           min_date=min_date, max_date=max_date)


@app.route('/report/total_sims_for_carrier')
def sims_for_carrier():
    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    if real_time_visualization:
        carriers = total_sims_for_carrier(min_date, max_date)

    else:
        stored_data = get_stored_data(min_date, max_date)
        carriers = db.session.query(Carrier).all()
        for carrier in carriers:
            carrier.sims_count = stored_data['sims_' + Carrier.carriers[carrier.name]]

    return render_template('report/sims_for_carrier.html', carriers=carriers,
                               min_date=min_date, max_date=max_date)


@app.route('/report/total_events_for_carrier')
def events_for_carrier():
    min_date = None
    max_date = None

    if request.args:
        min_date = get_min_date(request.args["min_date"], "%Y-%m-%d")
        max_date = get_max_date(request.args["max_date"], "%Y-%m-%d")

    if real_time_visualization:
        carriers = total_gsm_events_for_carrier(min_date, max_date)

    else:
        stored_data = get_stored_data(min_date, max_date)
        carriers = db.session.query(Carrier).all()
        for carrier in carriers:
            carrier.events_count = stored_data['events_' + Carrier.carriers[carrier.name]]

    return render_template('report/events_for_carrier.html', carriers=carriers,
                           min_date=min_date, max_date=max_date)
