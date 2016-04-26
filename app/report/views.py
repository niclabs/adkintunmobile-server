from flask import render_template

from app import app


@app.route('/report/')
def report_index():
    return render_template('report/index.html')


@app.route('/report/totales')
def total_devices_reported():
    from app.report.report import total_devices_reported
    from app.report.report import total_sims_registered
    from app.report.report import total_gsm_events

    total_devices = total_devices_reported()
    total_sims = total_sims_registered()
    total_events = total_gsm_events()
    return render_template('report/totales.html', total_devices=total_devices, total_sims=total_sims,
                           total_events=total_events)


@app.route('/report/total_device_for_carrier')
def device_for_carrier():
    from app.report.report import total_device_for_carrier

    carriers = total_device_for_carrier()
    return render_template('report/device_for_carrier.html', carriers=carriers)


@app.route('/report/total_sims_for_carrier')
def sims_for_carrier():
    from app.report.report import total_sims_for_carrier

    carriers = total_sims_for_carrier()
    return render_template('report/sims_for_carrier.html', carriers=carriers)


@app.route('/report/total_events_for_carrier')
def events_for_carrier():
    from app.report.report import total_events_for_carrier

    carriers = total_events_for_carrier()
    return render_template('report/events_for_carrier.html', carriers=carriers)
