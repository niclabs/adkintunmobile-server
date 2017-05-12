from flask_cors import cross_origin

from app import application

seconds_in_a_day = 60 * 60 * 24


@application.route("/connection_mode/<string:device_id>/<int:selected_day>", methods=["GET"])
@cross_origin()
def get_connectivity_event(device_id, selected_day):
    from app.models.connectivity_event import ConnectivityEvent
    from flask import jsonify
    from datetime import datetime

    events = ConnectivityEvent.query.filter(ConnectivityEvent.device_id == device_id,
                                            ConnectivityEvent.date >= datetime.fromtimestamp(selected_day),
                                            ConnectivityEvent.date < datetime.fromtimestamp(selected_day + seconds_in_a_day)).all()

    ret = [{'timestamp' : i.date.timestamp(),
            'connected' : i.connected,
            'type' : i.connection_type} for i in events]
    try:
        last_yesterday_event = \
            ConnectivityEvent.query.filter(ConnectivityEvent.device_id == device_id,
                                           ConnectivityEvent.date >= datetime.fromtimestamp(selected_day - seconds_in_a_day),
                                           ConnectivityEvent.date < datetime.fromtimestamp(selected_day)).\
                order_by(ConnectivityEvent.date.desc()).first()
        ret.append({'timestamp' : selected_day,
                    'connected' : last_yesterday_event.connected,
                    'type' : last_yesterday_event.connection_type})
    except AttributeError:
        pass

    return jsonify(ret), 200


@application.route("/network_type/<string:device_id>/<int:selected_day>", methods=["GET"])
@cross_origin()
def get_gsm_events(device_id, selected_day):
    from flask import jsonify
    from datetime import datetime
    from app.models.gsm_event import GsmEvent

    events = GsmEvent.query.filter(GsmEvent.device_id == device_id,
                                   GsmEvent.date >= datetime.fromtimestamp(selected_day),
                                   GsmEvent.date < datetime.fromtimestamp(selected_day + seconds_in_a_day)).all()

    ret = [{'timestamp' : i.date.timestamp(),
            'type' : i.network_type} for i in events]
    try:
        last_yesterday_event = GsmEvent.query.filter(GsmEvent.device_id == device_id,
                                                     GsmEvent.date >= datetime.fromtimestamp(selected_day - seconds_in_a_day),
                                                     GsmEvent.date < datetime.fromtimestamp(selected_day))\
            .order_by(GsmEvent.date.desc()).first()
        ret.append({'timestamp' : selected_day,
                    'type' : last_yesterday_event.network_type})
    except AttributeError:
        pass

    return jsonify(ret), 200


@application.route("/app_traffic/<string:device_id>/<int:actual_day>", methods=["GET"])
@cross_origin()
def get_app_traffic(device_id, actual_day):
    from flask import jsonify
    from datetime import datetime
    from app import db
    from app.models.application_traffic_event import ApplicationTrafficEvent
    from app.models.application import Application

    app_traffic = db.session.query(Application.id.label('id'),
                                   Application.package_name.label('name'),
                                   db.func.count(ApplicationTrafficEvent.id).label('count'),
                                   db.func.sum(ApplicationTrafficEvent.rx_bytes).label('rx_bytes'),
                                   db.func.sum(ApplicationTrafficEvent.tx_bytes).label('tx_bytes'),
                                   ApplicationTrafficEvent.network_type) \
        .filter(ApplicationTrafficEvent.device_id == device_id, ApplicationTrafficEvent.network_type == 1,
                ApplicationTrafficEvent.application_id == Application.id,
                ApplicationTrafficEvent.date >= datetime.fromtimestamp(actual_day - seconds_in_a_day*30)) \
        .group_by(Application.id, ApplicationTrafficEvent.network_type).all()
    ret = [{'app_id' : i.id,
            'app_name': i.name,
            'rx_bytes' : float(i.rx_bytes),
            'tx_bytes' : float(i.tx_bytes)} for i in app_traffic]

    return jsonify(ret), 200


@application.route("/monthly_app_traffic/<string:device_id>/<int:actual_day>/<int:app_id>", methods=["GET"])
@cross_origin()
def get_monthly_app_traffic(device_id, actual_day, app_id):
    from flask import jsonify
    from datetime import datetime
    from app import db
    from app.models.application_traffic_event import ApplicationTrafficEvent

    app_traffic = db.session.query(ApplicationTrafficEvent.rx_bytes,
                                   ApplicationTrafficEvent.tx_bytes,
                                   ApplicationTrafficEvent.date) \
        .filter(ApplicationTrafficEvent.device_id == device_id, ApplicationTrafficEvent.network_type == 1,
                ApplicationTrafficEvent.application_id == app_id,
                ApplicationTrafficEvent.date >= datetime.fromtimestamp(actual_day - seconds_in_a_day*30)) \
        .all()
    ret = [{'rx_bytes' : float(i.rx_bytes),
            'tx_bytes' : float(i.tx_bytes),
            'date': i.date.timestamp()} for i in app_traffic]

    return jsonify(ret), 200


def get_network_type(id):
    from app.models.speedtests.network_interface import NetworkInterface

    try:
        return NetworkInterface.query.get(id).active_interface
    except (TypeError, AttributeError):
        return -1


def get_network_type_details(id):
    from app.models.speedtests.network_interface import NetworkInterface

    try:
        ni = NetworkInterface.query.get(id)
        if ni.active_interface == 1:
            return ni.network_type
        else:
            return ni.ssid
    except (TypeError, AttributeError):
        return -1


@application.route("/speed_test/<string:device_id>", methods=["GET"])
@cross_origin()
def get_speed_test_reports(device_id):
    from flask import jsonify
    from app.models.speedtests.speed_test_report import SpeedTestReport

    reports = SpeedTestReport.query.filter(SpeedTestReport.device_id == device_id).all()
    ret = {'data': [{
                        'network_type' : get_network_type(i.network_interface_id),
                        'details' : get_network_type_details(i.network_interface_id),
                        'host' : i.host,
                        'download_speed': i.download_speed,
                        'download_size': i.download_size,
                        'upload_speed': i.upload_speed,
                        'upload_size': i.upload_size,
                        'date': i.date.timestamp()} for i in reports]}

    return jsonify(ret), 200


@application.route("/media_test/<string:device_id>", methods=["GET"])
@cross_origin()
def get_media_test_reports(device_id):
    from flask import jsonify
    from app.models.speedtests.media_test_report import MediaTestReport

    reports = MediaTestReport.query.filter(MediaTestReport.device_id == device_id).all()
    ret = {'data': [{
                        'network_type' : get_network_type(i.network_interface_id),
                        'details' : get_network_type_details(i.network_interface_id),
                        'results' : [{'quality' : j.quality,
                                      'buffering_time' : j.buffering_time,
                                      'loaded_fraction' : j.loaded_fraction,
                                      'downloaded_bytes' : j.downloaded_bytes} for j in i.video_results.all()],
                        'date': i.date.timestamp()} for i in reports]}
    return jsonify(ret), 200


@application.route("/connectivity_test/<string:device_id>", methods=["GET"])
@cross_origin()
def get_connectivity_test_reports(device_id):
    from flask import jsonify
    from app.models.speedtests.connectivity_test_report import ConnectivityTestReport

    reports = ConnectivityTestReport.query.filter(ConnectivityTestReport.device_id == device_id).all()
    ret = {'data': [{
                        'network_type' : get_network_type(i.network_interface_id),
                        'details' : get_network_type_details(i.network_interface_id),
                        'results' : [{'url' : j.url,
                                      'loaded' : j.loaded,
                                      'loading_time' : j.loading_time,
                                      'downloaded_bytes' : j.downloaded_bytes} for j in i.sites_results.all()],
                        'date': i.date.timestamp()} for i in reports]}
    return jsonify(ret), 200