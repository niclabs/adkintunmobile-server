from app import app
from app.models.application import Application
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.event import Event
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent
from app.models.wifi_traffic_event import WifiTrafficEvent
from config import AppTokens
from tests import base_test_case
from tests.events.normal_event_json import events_json


class SaveEventsTestCase(base_test_case.BaseTestCase):
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
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post('/api/events', data=dict(
                    events=events_json
            ), headers={'Authorization': 'token ' + token})

            assert request.status_code == 201
            # assert events
            events = Event.query.all()
            wifi_events = WifiTrafficEvent.query.all()
            state_events = StateChangeEvent.query.all()
            traffic_events = TrafficEvent.query.all()
            application_events = ApplicationTrafficEvent.query.all()
            mobile_events = MobileTrafficEvent.query.all()
            assert len(events) == 15

            # assert application event cl.niclabs.adkintunmobile
            application = Application.query.filter(Application.package_name == "cl.niclabs.adkintunmobile").first()
            assert application.package_name == "cl.niclabs.adkintunmobile"
            application_event = ApplicationTrafficEvent.query.filter(
                    ApplicationTrafficEvent.application == application).first()
            assert application_event.tx_bytes == 5615

            # assert mobile event
            assert len(mobile_events) == 3

            # TODO: Cambiar última comprobación por una diferencia de tiempo en vez de la fecha
