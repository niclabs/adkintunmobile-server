from datetime import datetime, timedelta

from app import application, db
from tests import base_test_case
from app.models.application import Application
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.sim import Sim
from app.report.application_report_generation import app_report


class ApplicationReportTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # applications
        app1 = Application("app1")
        app2 = Application("app2")
        app3 = Application("app3")

        # devices
        device1 = Device(device_id="1")
        device2 = Device(device_id="2")
        device3 = Device(device_id="3")

        # sims
        sim1 = Sim(carrier_id=1, serial_number="1")
        sim2 = Sim(carrier_id=2, serial_number="2")
        sim3 = Sim(carrier_id=2, serial_number="3")

        # application_traffic_events
        event0 = ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=1,
                                         tx_bytes=1, rx_bytes=2, network_type=6,
                                         date=datetime.now() + timedelta(days=-2))
        event1 = ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=1,
                                         tx_bytes=0, rx_bytes=1, network_type=6, date=datetime.now())
        event2 = ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=2,
                                         tx_bytes=3, rx_bytes=4, network_type=1, date=datetime.now())
        event3 = ApplicationTrafficEvent(device_id="2", sim_serial_number="2", application_id=2,
                                         tx_bytes=0, rx_bytes=2, network_type=1, date=datetime.now())
        event4 = ApplicationTrafficEvent(device_id="3", sim_serial_number="3", application_id=2,
                                         tx_bytes=2, rx_bytes=2, network_type=6, date=datetime.now())
        event5 = ApplicationTrafficEvent(device_id="3", sim_serial_number="3", application_id=3,
                                         tx_bytes=2, rx_bytes=1, network_type=1, date=datetime.now())

        device1.application_traffic_events = [event0, event1, event2]
        device2.application_traffic_events = [event3]
        device3.application_traffic_events = [event4, event5]
        sim1.devices.append(device1)
        sim2.devices.append(device2)
        sim3.devices.append(device3)

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.sims = [sim1]
        carrier2.sims = [sim2, sim3]

        db.session.add(app1)
        db.session.add(app2)
        db.session.add(app3)
        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_application_report_generation(self):
        with application.app_context():
            application_report = app_report(min_date=datetime.now() + timedelta(days=-1))
            application_report_expected = {
                1: {
                    "WIFI": {
                        "ALL": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}},
                        "UPLOAD": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "0.0", "total_bytes": "0"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}},
                    "MOBILE": {
                        "ALL": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "7.0", "total_bytes": "7"}},
                        "UPLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "3.0", "total_bytes": "3"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"}}}},
                2: {
                    "WIFI": {
                        "ALL": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"}},
                        "UPLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"}}},
                    "MOBILE": {
                        "ALL": {
                            1: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "3.0", "total_bytes": "3"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"}},
                        "UPLOAD": {
                            1: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "0.0", "total_bytes": "0"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            2: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}}},
                "ALL_CARRIERS": {
                    "WIFI": {
                        "ALL": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"},
                            2: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}},
                        "UPLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            2: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "0.0", "total_bytes": "0"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            2: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}},
                    "MOBILE": {
                        "ALL": {
                            1: {"app_name": "app2", "total_devices": 2, "bytes_per_user": "4.5", "total_bytes": "9"},
                            2: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "3.0", "total_bytes": "3"}},
                        "UPLOAD": {
                            1: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            2: {"app_name": "app2", "total_devices": 2, "bytes_per_user": "1.5", "total_bytes": "3"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app2", "total_devices": 2, "bytes_per_user": "3.0", "total_bytes": "6"},
                            2: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}}}
            }
            self.assertEqual(len(application_report), 3)
            carriers = [1, 2, "ALL_CARRIERS"]
            for carrier in carriers:
                self.assertIn(carrier, application_report)
                network_types = ["MOBILE", "WIFI"]
                for network_type in network_types:
                    self.assertIn(network_type, application_report[carrier])
                    connection_modes = ["ALL", "UPLOAD", "DOWNLOAD"]
                    for connection_mode in connection_modes:
                        self.assertIn(connection_mode, application_report[carrier][network_type])
                        fail_message = "Test failed for Carrier: %s, Network Type: %s, Mode: %s" % \
                                       (str(carrier), network_type, connection_mode)
                        self.assertDictEqual(application_report[carrier][network_type][connection_mode],
                                             application_report_expected[carrier][network_type][connection_mode],
                                             msg=fail_message)




