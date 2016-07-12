import gzip
import json
from datetime import datetime

from app import auth
from app import db, app
from app.api import api
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequestKeyError


class ReadEventsFromArgument(Resource):
    """
    Used for tests
    """
    method_decorators = [auth.login_required]

    def post(self):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('events', required=True)

        try:
            args = post_parser.parse_args()
            jsonvar = json.loads(args.events)
            device, sim, app_version_code = set_events_context(jsonvar)
            return read_events(jsonvar, device, sim, app_version_code)

        except (json.JSONDecodeError, BadRequestKeyError, UnicodeError) as e:
            return e, 400
        except (KeyError, Exception) as e:
            db.session.rollback()
            return e, 400


api.add_resource(ReadEventsFromArgument, '/api/events')


@app.route('/events', methods=['POST'])
@auth.login_required
def read_events_from_file():
    try:
        f = request.files['uploaded_file']

        # Uncompress Gzip file
        u = gzip.open(f, 'rb')

        lines = u.readlines()
        if not lines:
            return 'Bad Request: Empty File', 400
        string = ''.join(x.decode('utf-8') for x in lines)
        string = string.replace('\n', '')
        jsonvar = json.loads(string)
        device, sim, app_version_code = set_events_context(jsonvar)
        return read_events(jsonvar, device, sim, app_version_code)

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
        db.session.rollback()
    except Exception as e:
        app.logger.error("Unknow Exception: " + str(e))
        db.session.rollback()
    return 'Bad Request', 400


def read_events(jsonvar, device, sim, app_version_code):
    total_events = 0
    del jsonvar['device_records']
    del jsonvar['sim_records']

    for events_name, events in jsonvar.items():
        total_events += save(events_name, events, device, sim, app_version_code)
    app.logger.info('Eventos Almacenados: ' + str(total_events))

    return 'Events saved successfully', 201


def set_events_context(jsonvar):
    from app.models.device import Device
    device = Device.store_if_no_exist(jsonvar['device_records'])
    app_version_code = jsonvar['device_records']['app_version_code']

    from app.models.sim import Sim
    sim = Sim.store_if_not_exist(jsonvar['sim_records'])

    if sim:
        from app.models.carrier import Carrier
        carrier = Carrier.query.filter(
            Carrier.mnc == jsonvar['sim_records']['mnc'], Carrier.mcc == jsonvar['sim_records']['mcc']).first()

        # Link sim with device
        sim.add_device(device)

        # Link carrier with sim
        carrier.add_sim(sim)

        db.session.add(sim)
        db.session.add(carrier)

    db.session.commit()

    return device, sim, app_version_code


def save_traffics_events(events, device, sim, app_version_code):
    total_events = 0
    for event in events:
        total_events += 1
        event['app_version_code'] = app_version_code
        if event['event_type'] == 2:
            save_mobile_traffic_event(event, device, sim)
        elif event['event_type'] == 4:
            save_wifi_traffic_event(event, device, sim)
        elif event['event_type'] == 8:
            save_application_traffic_event(event, device, sim)
    return total_events


def save_application_traffic_event(event, device, sim):
    from app.models.application_traffic_event import ApplicationTrafficEvent
    from app.models.application import Application
    eventModel = ApplicationTrafficEvent()
    application = Application()
    for k, v in event.items():
        if k == 'timestamp':
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == 'package_name':
            application = Application.store_if_not_exist(v)
        elif k == 'id':
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)
    application.application_traffic_event.append(eventModel)
    store_event_in_db(eventModel, device, sim)


def save_wifi_traffic_event(event, device, sim):
    from app.models.wifi_traffic_event import WifiTrafficEvent

    eventModel = WifiTrafficEvent()

    for k, v in event.items():
        if k == 'timestamp':
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == 'id':
            continue
        elif hasattr(eventModel, k):
            setattr(eventModel, k, v)

    store_event_in_db(eventModel, device, sim)


def save_mobile_traffic_event(event, device, sim):
    from app.models.mobile_traffic_event import MobileTrafficEvent
    eventModel = MobileTrafficEvent()
    for k, v in event.items():

        if k == 'timestamp':
            eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
        elif k == 'id':
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
        event['app_version_code'] = app_version_code
        carrier = None
        for k, v in event.items():
            if k == 'timestamp':
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == 'signal_strength':
                # add new atributes of signal_strength
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'cdma_ecio':
                # add new atributes of cdma_ecio
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'evdo_dbm':
                # add new atributes of evdo_dbm
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'evdo_ecio':
                # add new atributes of evdo_ecio
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'evdo_snr':
                # add new atributes of evdo_snr
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'id':
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
        event['app_version_code'] = app_version_code
        eventModel = ConnectivityEvent()
        for k, v in event.items():

            if k == 'timestamp':
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == 'id':
                continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        store_event_in_db(eventModel, device, sim)
    return total_events


def save_gsm_events(events, device, sim, app_version_code):
    from app.models.gsm_event import GsmEvent
    from app.models.carrier import Carrier
    total_events = 0
    for event in events:
        total_events += 1
        event['app_version_code'] = app_version_code
        eventModel = GsmEvent()
        carrier = None
        for k, v in event.items():
            if k == 'timestamp':
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == 'signal_ber':
                # add new atributes of signal_ber
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'signal_strength':
                # add new atributes of signal_strength
                setattr(eventModel, k + '_size', event[k]['size'])
                setattr(eventModel, k + '_mean', event[k]['mean'])
                setattr(eventModel, k + '_variance', event[k]['variance'])
            elif k == 'id':
                continue
            elif k == 'mnc':
                try:
                    carrier = Carrier.query.filter(Carrier.mnc == v, Carrier.mcc == event['mcc']).first()
                except:
                    app.logger.error("Unkown Carrier: mnc:" + str(event[k]) + " , mcc:" + str(event['mcc']))
                    continue
            elif hasattr(eventModel, k):
                setattr(eventModel, k, v)

        if carrier:
            store_gsm_event_in_db(eventModel, device, sim, carrier)
        else:
            store_event_in_db(eventModel, device, sim)
    return total_events


def save_telephony_events(events, device, sim, app_version_code):
    return 0


def save_state_events(events, device, sim, app_version_code):
    from app.models.state_change_event import StateChangeEvent
    total_events = 0
    for event in events:
        total_events += 1
        event['app_version_code'] = app_version_code
        eventModel = StateChangeEvent()
        for k, v in event.items():

            if k == 'timestamp':
                eventModel.date = datetime.fromtimestamp(timestamp=v / 1000)
            elif k == 'id':
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
    if sim:
        sim.events.append(event)
        db.session.add(sim)
    db.session.add(event)
    db.session.add(device)
    db.session.commit()


def store_gsm_event_in_db(event, device, sim, carrier):
    from app.models.antenna import Antenna
    if event.gsm_lac and event.gsm_cid:
        antenna = Antenna.query.filter(Antenna.lac == event.gsm_lac, Antenna.cid == event.gsm_cid).first()
        if antenna:
            event.antennas.append(antenna)
        else:
            app.logger.error("Unkown Antenna: lac:" + str(event.gsm_lac) + " , cid:" + str(event.gsm_cid)+ ", mnc: "+ carrier.mnc + ", mcc: " + carrier.mcc)
    carrier.telephony_observation_events.append(event)
    db.session.add(carrier)
    store_event_in_db(event, device, sim)
