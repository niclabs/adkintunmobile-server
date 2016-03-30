from datetime import datetime

from dateutil.parser import parse

from app import app, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.sim import Sim
from app.models.connectivity_event import ConnectivityEvent
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
            connectivity_events = ConnectivityEvent.query.all()
            assert len(connectivity_events) == 1

            connectivity_event = connectivity_events[0]

            assert connectivity_event.available == True
            assert connectivity_event.connected == True
            assert connectivity_event.connection_type == 6
            assert connectivity_event.detailed_state == 4
            assert connectivity_event.date == datetime.fromtimestamp(1330641527540/1000).date()

            assert connectivity_event.sim.serial_number == 8956080124002959472
            assert connectivity_event.device.build_id == "JZO54K.I8190LUBAMH1"