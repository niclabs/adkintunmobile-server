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
                return read_and_save_events(jsonvar, device.device_id, sim.serial_number, app_version_code, session)
            else:
                return read_and_save_events(jsonvar, device.device_id, None, app_version_code, session)

        except (json.JSONDecodeError, BadRequestKeyError, UnicodeError) as e:
            return e, 400
        except (KeyError, Exception) as e:
            db.session.rollback()
            return e, 400


api.add_resource(ReadEventsFromArgument, "/api/events")


@app.route("/events", methods=["POST"])
@auth.login_required
def read_events_from_file():
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

        session = Session()

        if sim:
            return read_and_save_events(jsonvar, device.device_id, sim.serial_number, app_version_code, session)
        else:
            return read_and_save_events(jsonvar, device.device_id, None, app_version_code, session)

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


def read_and_save_events(jsonvar, device_id, sim_serial_number, app_version_code, session):
    total_events = 0
    del jsonvar["device_records"]
    del jsonvar["sim_records"]

    for events_name, events in jsonvar.items():
        total_events += add_events(events_name, events, device_id, sim_serial_number, app_version_code, session)

    try:
        # save and commit events and information to the database
        session.commit()
    except Exception as e:
        app.logger.error("Error adding events to database " + str(e))
        session.rollback()
        return "Bad Request", 400

    app.logger.info("Saved Events: " + str(total_events))

    return "Events saved successfully", 201


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


def save_traffics_events(events, device_id, sim_serial_number, app_version_code, session):
    total_events = 0
    for event in events:
        total_events += 1
        event["app_version_code"] = app_version_code
        if event["event_type"] == 2:
            save_mobile_traffic_event(event, device_id, sim_serial_number, session)
        elif event["event_type"] == 4:
            save_wifi_traffic_event(event, device_id, sim_serial_number, session)
        elif event["event_type"] == 8:
            save_application_traffic_event(event, device_id, sim_serial_number, session)
    return total_events


def save_application_traffic_event(event, device_id, sim_serial_number, session):
    from app.models.application_traffic_event import ApplicationTrafficEvent
    from app.models.application import Application
    eventModel = ApplicationTrafficEvent()
    application = Application()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "package_name":
            application = Application.get_app_or_add_it(v)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    application.application_traffic_event.append(eventModel)
    add_event_in_db(eventModel, device_id, sim_serial_number, session)


def save_wifi_traffic_event(event, device_id, sim_serial_number, session):
    from app.models.wifi_traffic_event import WifiTrafficEvent

    eventModel = WifiTrafficEvent()

    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)

    add_event_in_db(eventModel, device_id, sim_serial_number, session)


def save_mobile_traffic_event(event, device_id, sim_serial_number, session):
    from app.models.mobile_traffic_event import MobileTrafficEvent
    eventModel = MobileTrafficEvent()
    for k, v in event.items():
        if k == "timestamp":
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == "id":
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    add_event_in_db(eventModel, device_id, sim_serial_number, session)


def save_cdma_events(events, device_id, sim_serial_number, app_version_code, session):
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
        add_event_in_db(eventModel, device_id, sim_serial_number, session)

    return total_events


def save_connectivity_events(events, device_id, sim_serial_number, app_version_code, session):
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

        add_event_in_db(eventModel, device_id, sim_serial_number, session)
    return total_events


def save_gsm_events(events, device_id, sim_serial_number, app_version_code, session):
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
        carrier = link_observation_with_carrier(eventModel)
        if carrier:
            link_gsm_event_with_antenna(eventModel, device_id, sim_serial_number, session)
        else:
            add_event_in_db(eventModel, device_id, sim_serial_number, session)
    return total_events


def save_telephony_events(events, device_id, sim_serial_number, app_version_code, session):
    return 0


def save_state_events(events, device_id, sim_serial_number, app_version_code, session):
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

        add_event_in_db(eventModel, device_id, sim_serial_number, session)
    return total_events


events_names = {
    "traffic_records": save_traffics_events,
    "cdma_records": save_cdma_events,
    "connectivity_records": save_connectivity_events,
    "gsm_records": save_gsm_events,
    "telephony_records": save_telephony_events,
    "state_records": save_state_events,
}


def add_events(events_name, events, device_id, sim_serial_number, app_version_code, session):
    return events_names[events_name](events, device_id, sim_serial_number, app_version_code, session)


def add_event_in_db(event, device_id, sim_serial_number, session):
    """
    Add each event to the database, but not make a commit.
    Also, vinculate event with a sim and a device if can.
    """
    if device_id:
        event.device_id = device_id
    if sim_serial_number:
        event.sim_serial_number = sim_serial_number
    session.add(event)


def link_gsm_event_with_antenna(event, device_id, sim_serial_number, session):
    from app.models.antenna import Antenna
    if event.gsm_lac and event.gsm_cid and event.mcc and event.mnc:
        antenna = Antenna.get_antenna_or_add_it(
            args={"cid": event.gsm_cid, "lac": event.gsm_lac, "mnc": event.mnc, "mcc": event.mcc})
        event.antenna_id = antenna.id
        add_event_in_db(event, device_id, sim_serial_number, session)


def link_observation_with_carrier(event):
    if event.mnc and event.mcc:
        from app.models.carrier import Carrier
        carrier = Carrier.get_carrier_or_add_it(args={"mnc": event.mnc, "mcc": event.mcc})
        event.carrier_id = carrier.id
        return carrier
