from datetime import datetime, timedelta

from app import app, db
from app.models.device import Device
from app.models.state_change_event import StateChangeEvent
from app.report.report import total_devices_reported
from tests import base_test_case


class TotalDevicesReportedTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # devices
        device1 = Device(device_id="1", creation_date=datetime.now() + timedelta(days=-2))
        device2 = Device(device_id="2", creation_date=datetime.now())
        device3 = Device(device_id="3", creation_date=datetime.now())
        device4 = Device(device_id="4", creation_date=datetime.now())

        # Eventos
        event1 = StateChangeEvent()
        event2 = StateChangeEvent()
        event3 = StateChangeEvent()

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
            total_devices = total_devices_reported()
            assert total_devices == 2


    def test_date_filter(self):
        with app.app_context():
            total_devices = total_devices_reported(min_date=(datetime.now() + timedelta(days=-1)))
            assert total_devices == 1
