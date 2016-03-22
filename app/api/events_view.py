from flask import request

from . import app


@app.route("/send_file", methods=['POST'])
def read_events():
    import json
    f = request.files['events']
    lines = f.readlines()

    string = ' '.join(str(x) for x in lines)
    jsonvar = json.load(f)

    # TODO tomar device del json
    device = None
    for events in jsonvar:
        events_name = None
        save_events(events_name, events, device)

    return "hola"


def save_application_traffic_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_cdma_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_connectivity_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_gsm_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_mobile_traffic_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_state_change_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_telephony_observation_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


def save_wifi_traffic_events(events, device):
    for event in events:
        # TODO validar
        # TODO guardar
        pass  # TODO borrar pass


# TODO los nombres deben coincidir con json enviado por celular
events_names = {
    'traffic': save_application_traffic_events,
    'cdma': save_cdma_events,
    'connectivity': save_connectivity_events,
    'gsm': save_gsm_events,
    'mobile': save_mobile_traffic_events,
    'state': save_state_change_events,
    'observation': save_telephony_observation_events,
    'wifi': save_wifi_traffic_events
}


def save_events(events_name, events, device):
    events_names[events_name](events, device)
