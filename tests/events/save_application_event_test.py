from datetime import datetime
from app import app
from app.models.application import Application
from app.models.application_traffic_event import ApplicationTrafficEvent
from config import AppTokens
from manage_commands import populate
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json


class SaveApplicationEventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        populate()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post('/api/events', data=dict(
                events=events_json
            ), headers={'Authorization': 'token ' + token})

            assert request.status_code == 201

            application_events = ApplicationTrafficEvent.query.all()
            assert len(application_events) == 1

            application_event = application_events[0]

            assert application_event.network_type == 6
            assert application_event.rx_bytes == 5143
            assert application_event.rx_packets == 1234
            assert application_event.date.date() == datetime.fromtimestamp(1330641500267 / 1000).date()
            assert application_event.tx_bytes == 5615
            assert application_event.tx_packets == 123
            assert application_event.app_version_code == "0.0a"

            assert application_event.sim.serial_number == "8000000000000000000"
            assert application_event.device.device_id == "8000000000000000000"

            assert application_event.application.package_name == "cl.niclabs.adkintunmobile"

            apps = Application.query.all()
            assert len(apps) == 1

            application = apps[0]
            assert application.package_name == "cl.niclabs.adkintunmobile"
