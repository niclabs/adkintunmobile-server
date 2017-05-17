from app import application
from tests.populate_db.populate_methods import populate_standard_test
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.device import Device
from app.models.event import Event
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.sim import Sim
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent
from app.models.wifi_traffic_event import WifiTrafficEvent
from app.models.connectivity_event import ConnectivityEvent
from app.models.gsm_event import GsmEvent
from config import AppTokens
from tests import base_test_case
from tests.events.standard_event_without_sim_json import events_json


class SaveEventsWithoutSim(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        populate_standard_test()

    #  Saving events test: 1 wifi traffic event and 2 state change event
    def test_save_events_without_sim(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=events_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201

            device = Device.query.filter(Device.device_id == "800000000000000000000").first()
            sims = Sim.query.all()
            assert device
            assert len(sims) == 0

            # assert events
            wifi_events = WifiTrafficEvent.query.all()
            state_events = StateChangeEvent.query.all()
            connectivity_events = ConnectivityEvent.query.all()
            gsm_events = GsmEvent.query.all()
            application_events = ApplicationTrafficEvent.query.all()
            mobile_events = MobileTrafficEvent.query.all()
            # Check each table has the appropriate amount of rows
            assert len(state_events) == 2
            assert len(connectivity_events) == 1
            assert len(gsm_events) == 3
            assert len(application_events) == 3
            assert len(wifi_events) == 3
            assert len(mobile_events) == 3

            # assert device and sim are linked with the event
            all_events = [wifi_events, state_events, application_events,
                          mobile_events, connectivity_events, gsm_events]
            for events in all_events:
                for event in events:
                    assert device.device_id == event.device_id
                    assert event.sim_serial_number is None
