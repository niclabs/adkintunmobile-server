from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse
from . import api
from . import app
from .. import db


class ReadEvents(Resource):
    def post(self):
        import json
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('events', required=True)

        args = post_parser.parse_args()
        jsonvar = json.loads(args.events)

        from app.models.device import Device
        device = Device.store_if_no_exist(jsonvar["device_records"])
        app_version_code = jsonvar["device_records"]["app_version_code"]
        del jsonvar["device_records"]

        from app.models.sim import Sim
        sim = Sim.store_if_not_exist(jsonvar["sim_records"])
        del jsonvar["sim_records"]

        total_events = 0
        try:
            for events_name, events in jsonvar.items():
                total_events += save(events_name, events, device, sim, app_version_code)

            print("Eventos Almacenados: ", total_events)
        except Exception as e:
            db.session.rollback()
            return e, 400
        return '', 201


@app.route("/send_file", methods=['POST'])
def read_events():
    import json
    f = request.files['uploaded_file']
    lines = f.readlines()

    string = ''.join(x.decode("utf-8") for x in lines)

    string = string.replace('\n', '')
    jsonvar = json.loads(string)

    from app.models.device import Device
    device = Device.store_if_no_exist(jsonvar["device_records"])
    app_version_code = jsonvar["device_records"]["app_version_code"]
    del jsonvar["device_records"]

    from app.models.sim import Sim
    sim = Sim.store_if_not_exist(jsonvar["sim_records"])
    del jsonvar["sim_records"]

    total_events = 0
    try:
        for events_name, events in jsonvar.items():
            total_events += save(events_name, events, device, sim, app_version_code)
        print("Eventos Almacenados: ", total_events)
    except Exception as e:
        db.session.rollback()
        return e, 400
    return 'Eventos guardados', 201


api.add_resource(ReadEvents, '/api/send_file')


def save_traffics_events(events, device, sim, app_version_code):
    total_events = 0
    for event in events:
        total_events += 1
        event["app_version_code"] = app_version_code
        if event["event_type"] == 2:
            save_mobile_traffic_event(event, device, sim)
        elif event["event_type"] == 4:
            save_wifi_traffic_event(event, device, sim)
        elif event["event_type"] == 8:
            save_application_traffic_event(event, device, sim)
    return total_events


def save_application_traffic_event(event, device, sim):
    from app.models.application_traffic_event import ApplicationTrafficEvent
    from app.models.application import Application
    eventModel = ApplicationTrafficEvent()
    application = Application()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "package_name":
            application = Application.store_if_not_exist(v)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    application.application_traffic_event.append(eventModel)
    store_event_in_db(eventModel, device, sim)


def save_wifi_traffic_event(event, device, sim):
    from app.models.wifi_traffic_event import WifiTrafficEvent

    eventModel = WifiTrafficEvent()

    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)

    store_event_in_db(eventModel, device, sim)


def save_mobile_traffic_event(event, device, sim):
    from app.models.mobile_traffic_event import MobileTrafficEvent
    eventModel = MobileTrafficEvent()
    for k, v in event.items():

        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)

    store_event_in_db(eventModel, device, sim)


def save_cdma_events(events, device, sim, app_version_code):
    from app.models.cdma_event import CdmaEvent
    total_events = 0
    for event in events:
        total_events += 1
        eventModel = CdmaEvent()
        event["app_version_code"] = app_version_code

        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_strength":
                # agregar atributos de signal_strength
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "cdma_ecio":
                # agregar atributos de cdma_ecio
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "evdo_dbm":
                # agregar atributos de evdo_dbm
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "evdo_ecio":
                # agregar atributos de evdo_ecio
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "evdo_snr":
                # agregar atributos de evdo_snr
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)

    return total_events


def save_connectivity_events(events, device, sim, app_version_code):
    from app.models.connectivity_event import ConnectivityEvent
    total_events = 0
    for event in events:
        total_events += 1
        event["app_version_code"] = app_version_code
        eventModel = ConnectivityEvent()
        for k, v in event.items():

            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)
    return total_events


def save_gsm_events(events, device, sim, app_version_code):
    from app.models.gsm_event import GsmEvent
    total_events = 0
    for event in events:
        total_events += 1
        event["app_version_code"] = app_version_code
        eventModel = GsmEvent()
        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_ber":
                # agregar atributos de signal_ber
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "signal_strength":
                # agregar atributos de signal_strength
                setattr(eventModel, k + "_size", event[k]['size'])
                setattr(eventModel, k + "_mean", event[k]['mean'])
                setattr(eventModel, k + "_variance", event[k]['variance'])
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        # arreglar esta union
        # sim.carrier.telephony_observation_events.append(eventModel)
        store_event_in_db(eventModel, device, sim)
    return total_events


def save_telephony_events(events, device, sim, app_version_code):
    return 0


def save_state_events(events, device, sim, app_version_code):
    from app.models.state_change_event import StateChangeEvent
    total_events = 0
    for event in events:
        total_events += 1
        event["app_version_code"] = app_version_code
        eventModel = StateChangeEvent()
        for k, v in event.items():

            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)
    return total_events


events_names = {
    'traffic_records': save_traffics_events,
    'cdma_records': save_cdma_events,
    'connectivity_records': save_connectivity_events,
    'gsm_records': save_gsm_events,
    'telephony_records': save_telephony_events,
    'state_records': save_state_events,
}


def save(events_name, events, device, sim, app_version_code):
    return events_names[events_name](events, device, sim, app_version_code)


def store_event_in_db(event, device, sim):
    device.events.append(event)
    sim.events.append(event)
    db.session.add(sim)
    db.session.add(event)
    db.session.add(device)
    db.session.commit()
