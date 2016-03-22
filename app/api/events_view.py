from flask import request

from . import app
from . import api
from flask_restful import Resource, reqparse
from .. import db


class ReadEvents(Resource):
    def post(self):
        import json
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('events', required=True)

        args = post_parser.parse_args()
        jsonvar = json.loads(args.events)

        # TODO tomar device del json
        device = None
        for events in jsonvar:
            events_name = None
            save_events(events_name, events, device)

        return "hola"


@app.route("/send_file", methods=['POST'])
def read_events():
    import json
    f = request.files['events']
    lines = f.readlines()

    string = ''.join(x.decode("utf-8") for x in lines)
    string = string.replace('\n', '')
    jsonvar = json.loads(string)

    # TODO tomar device del json
    device = None
    for events in jsonvar:
        events_name = None
        save(events_name, events, device)

    return "hola"


api.add_resource(ReadEvents, '/api/send_file')


def save_events(model):
    def save_event_with_model(events, device):
        for event in events:
            eventModel = model()
            for k, v in event:
                setattr(eventModel, k, v)

            device.events.append(eventModel)
            device.sim.events.append(eventModel)
            db.session.add(eventModel)
            db.session.add(device)
            db.session.commit()

    return save_event_with_model


def save_observations(model):
    def save_event_with_model(events, device):
        for event in events:
            eventModel = model()
            for k, v in event:
                setattr(eventModel, k, v)

            device.events.append(eventModel)
            device.sim.events.append(eventModel)
            device.sim.carrier.telephony_observation_events.append(eventModel)
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
from app.models.wifi_traffic_event import WifiTrafficEvent

events_names = {
    'traffic': save_events(ApplicationTrafficEvent),
    'cdma': save_observations(CdmaEvent),
    'connectivity': save_events(ConnectivityEvent),
    'gsm': save_observations(GsmEvent),
    'mobile': save_events(MobileTrafficEvent),
    'state': save_events(StateChangeEvent),
    'wifi': save_events(WifiTrafficEvent)
}


def save(events_name, events, device):
    events_names[events_name](events, device)
