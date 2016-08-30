import gzip
import json
from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequestKeyError

from app import db, app, auth, Session
from app.api import api


class ReadEventsFromArgument(Resource):
    """
    Used for tests
    """
    method_decorators = [auth.login_required]

    def post(self):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument("events", required=True)

        try:
            args = post_parser.parse_args()
            jsonvar = json.loads(args.events)
            device, sim, app_version_code = set_events_context(jsonvar)
            session = Session()
            if sim:
                return prepare_events(jsonvar, device.device_id, sim.serial_number, app_version_code)
            else:
                return prepare_events(jsonvar, device.device_id, None, app_version_code)

        except (json.JSONDecodeError, BadRequestKeyError, UnicodeError) as e:
            return e, 400
        except (KeyError, Exception) as e:
            db.session.rollback()
            return e, 400


api.add_resource(ReadEventsFromArgument, "/api/events")


@app.route("/events", methods=["POST"])
@auth.login_required
def save_events_from_file():
    try:
        f = request.files["uploaded_file"]

        # Uncompress Gzip file
        u = gzip.open(f, "rb")

        lines = u.readlines()
        if not lines:
            return "Bad Request: Empty File", 400
        string = "".join(x.decode("utf-8") for x in lines)
        string = string.replace("\n", "")
        jsonvar = json.loads(string)
        device, sim, app_version_code = set_events_context(jsonvar)

        if sim:
            events = prepare_events(jsonvar, device.device_id, sim.serial_number, app_version_code)
        else:
            events = prepare_events(jsonvar, device.device_id, None, app_version_code)

        # Seguir aquí con el procesamiento de eventos

        # try:
        #     # save and commit events and information to the database
        #     session.commit()
        # except Exception as e:
        #     app.logger.error("Error adding events to database " + str(e))
        #     session.rollback()
        #     return "Bad Request", 400
        #
        # app.logger.info("Saved Events: " + len(list_events))
        #
        # return "Events saved successfully", 201
        pass

    except json.JSONDecodeError as e:
        app.logger.error("JSONDecodeError: " + str(e))
    except BadRequestKeyError as e:
        app.logger.error("BadRequestKeyError: " + str(e))
    except UnicodeError as e:
        app.logger.error("UnicodeError: " + str(e))
    except TypeError as e:
        app.logger.error("TypeError: " + str(e))
    except KeyError as e:
        app.logger.error("KeyError: " + str(e))
    except Exception as e:
        app.logger.error("Unknow Exception: " + str(e))
    return "Bad Request", 400


def prepare_events(jsonvar, device_id, sim_serial_number, app_version_code):
    """
    Analyses all the events and add each one to a list. Also, set the context of each event, saving antennas,
    applications and all the others necessary objects.

    :param jsonvar: all events
    :param device_id: -
    :param sim_serial_number: -
    :param app_version_code: -
    :return: A list with all the events to save
    """
    list_events = []
    del jsonvar["device_records"]
    del jsonvar["sim_records"]

    for events_name, events in jsonvar.items():
        add_events_to_list(events_name, events, device_id, sim_serial_number, app_version_code, list_events)

    return list_events


def set_events_context(jsonvar):
    from app.models.device import Device
    device = Device.get_device_or_add_it(jsonvar["device_records"])
    app_version_code = jsonvar["device_records"]["app_version_code"]

    from app.models.sim import Sim
    sim = Sim.get_sim_or_add_it(jsonvar["sim_records"])
    session = Session()

    # Get carrier or add it, if it does not exist
    from app.models.carrier import Carrier
    carrier = Carrier.get_carrier_or_add_it(jsonvar["sim_records"])

    # Link sim with device
    sim.add_device(device)

    # Link carrier with sim
    carrier.add_sim(sim)

    session.add(sim)
    session.add(carrier)

    # add new device, sim or carrier
    session.commit()

    return device, sim, app_version_code


def store_traffics_events(events, device_id, sim_serial_number, app_version_code, list_events):
    for event in events:
        event["app_version_code"] = app_version_code
        if event["event_type"] == 2:
            store_mobile_traffic_event(event, device_id, sim_serial_number, list_events)
        elif event["event_type"] == 4:
            store_wifi_traffic_event(event, device_id, sim_serial_number, list_events)
        elif event["event_type"] == 8:
            store_application_traffic_event(event, device_id, sim_serial_number, list_events)


def store_application_traffic_event(event, device_id, sim_serial_number, list_events):
    from app.models.application_traffic_event import ApplicationTrafficEvent
    from app.models.application import Application
    eventModel = ApplicationTrafficEvent()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "package_name":
            application = Application.get_app_or_add_it(v)
            eventModel.application_id = application.id
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
    list_events.append(eventModel)


def store_wifi_traffic_event(event, device_id, sim_serial_number, list_events):
    from app.models.wifi_traffic_event import WifiTrafficEvent
    eventModel = WifiTrafficEvent()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
    list_events.append(eventModel)


def store_mobile_traffic_event(event, device_id, sim_serial_number, list_events):
    from app.models.mobile_traffic_event import MobileTrafficEvent
    eventModel = MobileTrafficEvent()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
    list_events.append(eventModel)


def store_cdma_events(events, device_id, sim_serial_number, app_version_code, list_events):
    from app.models.cdma_event import CdmaEvent
    for event in events:
        eventModel = CdmaEvent()
        event["app_version_code"] = app_version_code
        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_strength":
                # add new atributes of signal_strength
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "cdma_ecio":
                # add new atributes of cdma_ecio
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "evdo_dbm":
                # add new atributes of evdo_dbm
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "evdo_ecio":
                # add new atributes of evdo_ecio
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "evdo_snr":
                # add new atributes of evdo_snr
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)
        link_observation_with_carrier(eventModel)
        vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
        list_events.append(eventModel)


def store_connectivity_events(events, device_id, sim_serial_number, app_version_code, list_events):
    from app.models.connectivity_event import ConnectivityEvent
    for event in events:
        event["app_version_code"] = app_version_code
        eventModel = ConnectivityEvent()

        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)
        vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
        list_events.append(eventModel)


def store_gsm_events(events, device_id, sim_serial_number, app_version_code, list_events):
    from app.models.gsm_event import GsmEvent
    for event in events:
        event["app_version_code"] = app_version_code
        eventModel = GsmEvent()
        for k, v in event.items():
            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "signal_ber":
                # add new atributes of signal_ber
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "signal_strength":
                # add new atributes of signal_strength
                setattr(eventModel, k + "_size", event[k]["size"])
                setattr(eventModel, k + "_mean", event[k]["mean"])
                setattr(eventModel, k + "_variance", event[k]["variance"])
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)
        link_observation_with_carrier(eventModel)
        link_gsm_event_with_antenna(eventModel, device_id, sim_serial_number)
        vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
        list_events.append(eventModel)


def save_telephony_events(events, device_id, sim_serial_number, app_version_code, list_events):
    return 0


def save_state_events(events, device_id, sim_serial_number, app_version_code, list_events):
    from app.models.state_change_event import StateChangeEvent
    for event in events:
        event["app_version_code"] = app_version_code
        eventModel = StateChangeEvent()
        for k, v in event.items():

            if k == "timestamp":
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == "id":
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        vinculate_event_device_sim(eventModel, device_id, sim_serial_number)
        list_events.append(eventModel)


events_names = {
    "traffic_records": store_traffics_events,
    "cdma_records": store_cdma_events,
    "connectivity_records": store_connectivity_events,
    "gsm_records": store_gsm_events,
    "telephony_records": save_telephony_events,
    "state_records": save_state_events,
}


def add_events_to_list(events_name, events, device_id, sim_serial_number, app_version_code, list_events):
    return events_names[events_name](events, device_id, sim_serial_number, app_version_code, list_events)


def vinculate_event_device_sim(event, device_id, sim_serial_number):
    """
    Vinculate event with a sim and a device if can.
    """
    if device_id:
        event.device_id = device_id
    if sim_serial_number:
        event.sim_serial_number = sim_serial_number


def link_gsm_event_with_antenna(event, device_id, sim_serial_number):
    from app.models.antenna import Antenna

    if event.gsm_lac and event.gsm_cid and event.mcc and event.mnc:
        antenna = Antenna.get_antenna_or_add_it(
            args={"cid": event.gsm_cid, "lac": event.gsm_lac, "mnc": event.mnc, "mcc": event.mcc})
        event.antenna_id = antenna.id


def link_observation_with_carrier(event):
    if event.mnc and event.mcc:
        from app.models.carrier import Carrier
        carrier = Carrier.get_carrier_or_add_it(args={"mnc": event.mnc, "mcc": event.mcc})
        event.carrier_id = carrier.id

