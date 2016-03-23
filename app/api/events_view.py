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


def save_events(model):
    def save_event_with_model(events, device, sim):
        for event in events:
            eventModel = model()
            for k, v in event.items():
                if hasattr(eventModel, k):
                    if k == "timestamp":
                        v = datetime.fromtimestamp(timestamp=v)
                    setattr(eventModel, k, v)
            device.events.append(eventModel)
            sim.events.append(eventModel)
            db.session.add(sim)
            db.session.add(eventModel)
            db.session.add(device)
            db.session.commit()

    return save_event_with_model


def save_observations(model):
    def save_event_with_model(events, device, sim):
        for event in events:
            eventModel = model()
            for k, v in event.items():
                if hasattr(eventModel, 'k'):
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

    return save_event_with_model


from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.cdma_event import CdmaEvent
from app.models.connectivity_event import ConnectivityEvent
from app.models.gsm_event import GsmEvent
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent
from app.models.wifi_traffic_event import WifiTrafficEvent

events_names = {
    'traffic_records': save_events(ApplicationTrafficEvent),
    'cdma_records': save_observations(CdmaEvent),
    'connectivity': save_events(ConnectivityEvent),
    'gsm_records': save_observations(GsmEvent),
    'telephony_records': save_events(MobileTrafficEvent),
    'state_records': save_events(StateChangeEvent),
    'wifi_records': save_events(WifiTrafficEvent)
}


def save(events_name, events, device, sim):
    events_names[events_name](events, device, sim)
