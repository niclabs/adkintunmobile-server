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
    pass


def save_application_traffic_event(events, device, sim):
    pass


def save_wifi_traffic_event(events, device, sim):
    pass


def save_mobile_traffic_event(events, device, sim):
    pass


def save_cdma_events(events, device, sim):
    pass


def save_connectivity_events(events, device, sim):
    pass


def save_gsm_events(events, device, sim):
    pass


def save_telephony_events(events, device, sim):
    pass


def save_state_events(events, device, sim):
    from app.models.state_change_event import StateChangeEvent
    for event in events:
        eventModel = StateChangeEvent()
        for k, v in event.items():
            if hasattr(eventModel, k):
                if k == "timestamp":
                    v = datetime.fromtimestamp(timestamp=v)
                setattr(eventModel, k, v)

        device.events.append(eventModel)
        sim.events.append(eventModel)
        sim.carrier.telephony_observation_events.append(eventModel)
        db.session.add(sim)
        db.session.add(eventModel)
        db.session.add(device)
        db.session.commit()

events_names = {
    'traffic_records': save_traffics_events,
    'cdma_records': save_cdma_events,
    'connectivity': save_connectivity_events,
    'gsm_records': save_gsm_events,
    'telephony_records': save_telephony_events,
    'state_records': save_state_events
}


def save(events_name, events, device, sim):
    events_names[events_name](events, device, sim)
