from app import application
from app.data.populate_methods import populate_standard_test
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.device import Device
from app.models.event import Event
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.sim import Sim
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent
from app.models.wifi_traffic_event import WifiTrafficEvent
from config import AppTokens
from tests import base_test_case
from tests.events.standard_event_json import events_json


class SaveEventsWithDeviceAndSimTestCase(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        populate_standard_test()

    #  Saving events test: 1 wifi traffic event and 2 state change event
    def test_save_events_with_device_and_sim(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=events_json
            ), headers={"Authorization": "token " + token})

            device = Device.query.filter(Device.device_id == "800000000000000000000").first()
            sim = Sim.query.filter(Sim.serial_number == "800000000000000000000").first()
            assert device
            assert sim
            assert request.status_code == 201
            # assert events
            events = Event.query.all()
            wifi_events = WifiTrafficEvent.query.all()
            state_events = StateChangeEvent.query.all()
            traffic_events = TrafficEvent.query.all()
            application_events = ApplicationTrafficEvent.query.all()
            mobile_events = MobileTrafficEvent.query.all()
            assert len(events) == 15

            # assert device and sim are linked with the event
            all_events = [wifi_events, state_events, traffic_events, application_events, mobile_events]
            for events in all_events:
                for event in events:
                    assert device.device_id == event.device_id
                    assert sim.serial_number == event.sim_serial_number
