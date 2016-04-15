from datetime import datetime
from app import app
from app.models.wifi_traffic_event import WifiTrafficEvent
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json
from config import AppTokens
from tests.events import send_json_for_test

class SaveWifiEventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        pass

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            request = send_json_for_test(self, events_json, list(AppTokens.tokens.keys())[0])

            assert request.status_code == 201
            wifi_events = WifiTrafficEvent.query.all()
            assert len(wifi_events) == 1

            wifi_event = wifi_events[0]

            assert wifi_event.network_type == 6
            assert wifi_event.rx_bytes == 2361
            assert wifi_event.rx_packets == 19
            assert wifi_event.tcp_rx_bytes == 4532
            assert wifi_event.tcp_tx_bytes == 1523
            assert wifi_event.date == datetime.fromtimestamp(1330641510326 / 1000).date()
            assert wifi_event.tx_bytes == 196
            assert wifi_event.tx_packets == 4
            assert wifi_event.app_version_code == "0.0a"

            assert wifi_event.sim.serial_number == "8000000000000000000"
            assert wifi_event.device.device_id == "8000000000000000000"
