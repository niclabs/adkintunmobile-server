from datetime import datetime

from app import app
from app.models.gsm_event import GsmEvent
from app.models.carrier import Carrier
from config import AppTokens
from manage_commands import populate
from tests import base_test_case
from tests.events.one_event_in_type_json import events_json


class SaveGsmObservationEventTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        '''
        Populate the model with test data
        '''
        # Create the default sim
        populate()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_save_normal_events(self):
        with app.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post('/api/events', data=dict(
                events=events_json
            ), headers={'Authorization': 'token ' + token})

            assert request.status_code == 201
            gsm_events = GsmEvent.query.all()
            assert len(gsm_events) == 1

            gsm_event = gsm_events[0]

            assert gsm_event.network_type == 15
            assert gsm_event.telephony_standard == 1
            assert gsm_event.signal_strength_size == None
            assert gsm_event.signal_strength_mean == None
            assert gsm_event.signal_strength_variance == None
            assert gsm_event.gsm_cid == 1259355
            assert gsm_event.gsm_lac == 55700
            assert gsm_event.gsm_psc == -1
            assert gsm_event.signal_ber_size == None
            assert gsm_event.signal_ber_mean == None
            assert gsm_event.signal_ber_variance == None


            assert gsm_event.app_version_code == "0.0a"

            assert gsm_event.sim.serial_number == "8000000000000000000"
            assert gsm_event.device.device_id == "8000000000000000000"

            real_carrier = Carrier.query.filter(Carrier.mcc == 730, Carrier.mnc == 2).first()
            real_carrier.telephony_observation_events.first().id == gsm_event.id


