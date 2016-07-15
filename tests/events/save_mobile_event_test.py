from datetime import datetime

from app import app
from app.models.mobile_traffic_event import MobileTrafficEvent
from config import AppTokens
from manage_commands import populate
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json


class SaveMobileEventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        # Create the default sim
        populate()

    # test de guardado de eventos: 1 wifi traffic event and 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post('/api/events', data=dict(
                events=events_json
            ), headers={'Authorization': 'token ' + token})

            assert request.status_code == 201
            mobile_events = MobileTrafficEvent.query.all()
            assert len(mobile_events) == 1

            mobile_event = mobile_events[0]

            assert mobile_event.network_type == 1
            assert mobile_event.rx_bytes == 1234
            assert mobile_event.rx_packets == 45672
            assert mobile_event.tcp_rx_bytes == 4687
            assert mobile_event.tcp_tx_bytes == 1357
            assert mobile_event.date.date() == datetime.fromtimestamp(1330641500183 / 1000).date()
            assert mobile_event.tx_bytes == 489
            assert mobile_event.tx_packets == 35
            assert mobile_event.app_version_code == "0.0a"

            assert mobile_event.sim.serial_number == "8000000000000000000"
            assert mobile_event.device.device_id == "8000000000000000000"
