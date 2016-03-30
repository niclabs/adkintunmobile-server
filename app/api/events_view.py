from flask import request

from app.models.device import Device
from app.models.sim import Sim
from . import app
from . import api
from flask_restful import Resource, reqparse
from .. import db
from datetime import datetime


class ReadEvents(Resource):
    def post(self):
        import json
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('events', required=True)

        args = post_parser.parse_args()
        jsonvar = json.loads(args.events)
        device = Device.query.filter(Device.build_id == jsonvar["device_records"]["build_id"]).first()
        sim = Sim.query.filter(Sim.serial_number == jsonvar["sim_records"]["serial_number"]).first()
        del jsonvar["device_records"]
        del jsonvar["sim_records"]
        try:
            for events_name, events in jsonvar.items():
                save(events_name, events, device, sim)

        except Exception as e:
            db.session.rollback()
            return e, 400
        return '', 201


@app.route("/send_file", methods=['POST'])
def read_events():
    import json
    f = request.files['events']
    lines = f.readlines()

    string = ''.join(x.decode("utf-8") for x in lines)
    string = string.replace('\n', '')
    jsonvar = json.loads(string)
    device = Device.query.filter(Device.device == jsonvar["device_records"]["build_id"]).first()
    sim = Sim.query.filter(Sim.serial_number == jsonvar["sim_records"]["serial_number"]).first()
    del jsonvar["device_records"]
    del jsonvar["sim_records"]
    try:
        for events in jsonvar:
            events_name = None
            save(events_name, events, device, sim)

    except Exception as e:
        db.session.rollback()
        return e, 400
    return 'Eventos guardados', 201


api.add_resource(ReadEvents, '/api/send_file')


def save_traffics_events(events, device, sim):
    for event in events:
        if event["event_type"] == 2:
            save_mobile_traffic_event(event, device, sim)
        elif event["event_type"] == 4:
            save_wifi_traffic_event(event, device, sim)
        elif event["event_type"] == 8:
            save_application_traffic_event(event, device, sim)


def save_application_traffic_event(event, device, sim):
    from app.models.application_traffic_event import ApplicationTrafficEvent
    eventModel = ApplicationTrafficEvent()
    for k, v in event.items():

        if hasattr(eventModel, k):
            setattr(eventModel, k, v)
            continue

        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            continue

        if k == "package_name":
            addApplication(v, eventModel)
            continue

    store_event_in_db(eventModel, device, sim)


def addApplication(packageName, eventModel):
    from app.models.application import Application
    application = Application.query.filter(Application.package_name == packageName).first()
    if not application:
        application = Application(package_name=packageName)
        db.session.add(application)
    eventModel.application = application


def save_wifi_traffic_event(event, device, sim):
    from app.models.wifi_traffic_event import WifiTrafficEvent

    eventModel = WifiTrafficEvent()

    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        if hasattr(eventModel, k):
            setattr(eventModel, k, v)

    store_event_in_db(eventModel, device, sim)


def save_mobile_traffic_event(event, device, sim):
    from app.models.mobile_traffic_event import MobileTrafficEvent
    eventModel = MobileTrafficEvent()
    for k, v in event.items():

        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            continue

        if hasattr(eventModel, k):
            setattr(eventModel, k, v)
            continue

    store_event_in_db(eventModel, device, sim)


def save_cdma_events(events, device, sim):
    from app.models.cdma_event import CdmaEvent

    for event in events:
        eventModel = CdmaEvent()

        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_strength":
                #agregar atributos de signal_strength
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif k == "cdma_ecio":
                #agregar atributos de cdma_ecio
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif k == "evdo_dbm":
                #agregar atributos de evdo_dbm
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif k == "evdo_ecio":
                #agregar atributos de evdo_ecio
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif k == "evdo_snr":
                #agregar atributos de evdo_snr
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])

            if hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)


def save_connectivity_events(events, device, sim):
    from app.models.connectivity_event import ConnectivityEvent

    for event in events:
        eventModel = ConnectivityEvent()
        for k, v in event.items():

            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
                continue

            if k == "id":
                continue

            if hasattr(eventModel, k):
                setattr(eventModel, k, v)
                continue

        device.events.append(eventModel)
        sim.events.append(eventModel)
        db.session.add(sim)
        db.session.add(eventModel)
        db.session.add(device)
        db.session.commit()


def save_gsm_events(events, device, sim):
    from app.models.gsm_event import GsmEvent

    for event in events:
        eventModel = GsmEvent()
        for k, v in event.items():
            if k == "timestamp":
                v = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_ber":
                #agregar atributos de signal_ber
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif k == "signal_strength":
                #agregar atributos de signal_strength
                setattr(eventModel, k+"_size", event[k]['size'])
                setattr(eventModel, k+"_mean", event[k]['mean'])
                setattr(eventModel, k+"_variance", event[k]['variance'])
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        #arreglar esta union
        #sim.carrier.telephony_observation_events.append(eventModel)
        store_event_in_db(eventModel, device, sim)

def save_telephony_events(events, device, sim):
    pass


def save_state_events(events, device, sim):
    from app.models.state_change_event import StateChangeEvent
    for event in events:
        eventModel = StateChangeEvent()
        for k, v in event.items():

            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)

            if hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)

events_names = {
    'traffic_records': save_traffics_events,
    'cdma_records': save_cdma_events,
    'connectivity_records': save_connectivity_events,
    'gsm_records': save_gsm_events,
    'telephony_records': save_telephony_events,
    'state_records': save_state_events,
}


def save(events_name, events, device, sim):
    events_names[events_name](events, device, sim)

def store_event_in_db(event, device, sim):
        device.events.append(event)
        sim.events.append(event)
        db.session.add(sim)
        db.session.add(event)
        db.session.add(device)
        db.session.commit()