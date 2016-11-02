from app import application
from tests.populate_db.populate_methods import populate_standard_test
from app.models.carrier import Carrier
from app.models.gsm_event import GsmEvent
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.sim import Sim
from config import AppTokens
from tests import base_test_case
from tests.events.new_telco_events import events_json


class SaveNewTelcoEventsTestCase(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        # Create the default sim
        populate_standard_test()

    # Saving event test: 1 gsm observation event and 1 state record, both whit a non-existent telco
    def test_save_new_telco_events(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=events_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201

            gsm_events = GsmEvent.query.all()
            assert len(gsm_events) == 1
            gsm_event = gsm_events[0]

            mobile_events = MobileTrafficEvent.query.all()
            assert len(mobile_events) == 1

            sim = Sim.query.filter(Sim.serial_number == "800000000000000000000").first()
            assert sim

            carrier = Carrier.query.filter(Carrier.mnc == 9, Carrier.mcc == 120).first()
            assert carrier

            assert sim.carrier.mnc == 9
            assert sim.carrier.mcc == 120

            assert len(carrier.telephony_observation_events.all()) == 1

            assert carrier.telephony_observation_events[0].id == gsm_event.id
