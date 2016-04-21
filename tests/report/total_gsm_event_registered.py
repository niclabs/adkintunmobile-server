from app import app, db
from app.models.device import Device
from app.models.gsm_event import GsmEvent
from app.report.report import total_gsm_events
from tests import base_test_case


class TotalSimsRegisteredTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # devices
        device1 = Device(device_id="1")
        device2 = Device(device_id="2")
        device3 = Device(device_id="3")
        device4 = Device(device_id="4")

        # GSM events
        event1 = GsmEvent()
        event2 = GsmEvent()
        event3 = GsmEvent()

        device1.events = [event1, event2]
        device2.events = [event3]
        device3.events = []

        db.session.add(device1)
        db.session.add(device2)
        db.session.add(device3)
        db.session.add(device4)
        db.session.commit()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_two_devices(self):
        with app.app_context():
            gsm_events = total_gsm_events()
            assert gsm_events == 3
