from datetime import datetime

from dateutil.parser import parse

from app import app, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.sim import Sim
from app.models.wifi_traffic_event import WifiTrafficEvent
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json


class EventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        # Create the default sim
        carrier = Carrier("test", 1, 456)
        sim = Sim(creation_date=parse('04/02/2016'), serial_number=8956080124002959472)

        device = Device(
                brand="brand test",
                board="board test",
                build_id="JZO54K.I8190LUBAMH1",
                device="device test",
                hardware="hardware test",
                manufacturer="manufacturer test",
                model="model test",
                release="release test",
                release_type="release type test",
                product="product test",
                sdk=4,
                creation_date=datetime.now().date())
        try:
            db.session.add(carrier)
            db.session.add(sim)
            db.session.add(device)
            carrier.sims.append(sim)
            sim.devices.append(device)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            request = self.app.post('/api/send_file', data=dict(
                    events=events_json
            ))

            assert request.status_code == 201
            wifi_events = WifiTrafficEvent.query.all()
            assert len(wifi_events) == 1

            wifi_event = wifi_events[0]

            assert wifi_event.network_type == 6
            assert wifi_event.rx_bytes == 2361
            assert wifi_event.rx_packets == 19
            assert wifi_event.tcp_rx_bytes == 4532
            assert wifi_event.tcp_tx_bytes == 1523
            assert wifi_event.date == datetime.fromtimestamp(1330641510326/1000).date()
            assert wifi_event.tx_bytes == 196
            assert wifi_event.tx_packets == 4

            assert wifi_event.sim.serial_number == 8956080124002959472
            assert wifi_event.device.build_id == "JZO54K.I8190LUBAMH1"