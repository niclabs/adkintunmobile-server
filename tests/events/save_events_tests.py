from datetime import datetime

from app import app, db
from tests import base_test_case
from tests.events.normal_event_json import events_json
from app.models.carrier import Carrier
from app.models.sim import Sim
from app.models.device import Device
from app.models.wifi_traffic_event import WifiTrafficEvent
from app.models.state_change_event import StateChangeEvent
from app.models.mobile_traffic_event import MobileTrafficEvent
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.application import Application
from app.models.traffic_event import TrafficEvent
from app.models.event import Event
from dateutil.parser import parse


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

            #assert mobile event
            assert len(mobile_events) == 3

            # TODO: Cambiar última comprobación por una diferencia de tiempo en vez de la fecha
