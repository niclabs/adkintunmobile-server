from datetime import datetime, timedelta
from app import application, db
from app.models.device import Device
from app.models.state_change_event import StateChangeEvent
from app.report.general_report_generation import total_devices_registred
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
        event1 = StateChangeEvent(date=datetime.now())
        event2 = StateChangeEvent(date=datetime.now())
        event3 = StateChangeEvent(date=datetime.now())

        device1.state_change_events = [event1, event2]
        device2.state_change_events = [event3]
        device3.state_change_events = []

        db.session.add(device1)
        db.session.add(device2)
        db.session.add(device3)
        db.session.add(device4)
        db.session.commit()

    def test_two_devices(self):
        with application.app_context():
            total_devices = total_devices_registred()
            self.assertEqual(total_devices, 4)

    def test_date_filter(self):
        with application.app_context():
            total_devices = total_devices_registred(min_date=(datetime.now() + timedelta(days=-1)))
            self.assertEqual(total_devices, 3)
