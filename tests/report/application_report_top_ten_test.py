from datetime import datetime, timedelta

from app import application, db
from tests import base_test_case
from app.models.application import Application
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.sim import Sim
from app.report.application_report_generation import app_report


class ApplicationReportTopTenTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # applications
        apps = [Application("app1"), Application("app2"), Application("app3"), Application("app4"),
                Application("app5"), Application("app6"), Application("app7"), Application("app8"),
                Application("app9"), Application("app10"), Application("app11")]

        # devices
        device1 = Device(device_id="1")

        # sims
        sim1 = Sim(carrier_id=1, serial_number="1")
        sim1.devices.append(device1)

        # application_traffic_events

        events = [
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=1,
                                    tx_bytes=1, rx_bytes=512, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=2,
                                    tx_bytes=2, rx_bytes=256, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=3,
                                    tx_bytes=3, rx_bytes=128, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=4,
                                    tx_bytes=4, rx_bytes=64, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=5,
                                    tx_bytes=5, rx_bytes=32, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=6,
                                    tx_bytes=6, rx_bytes=16, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=7,
                                    tx_bytes=7, rx_bytes=8, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=8,
                                    tx_bytes=8, rx_bytes=4, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=9,
                                    tx_bytes=9, rx_bytes=2, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=10,
                                    tx_bytes=10, rx_bytes=1, network_type=1, date=datetime.now()),
            ApplicationTrafficEvent(device_id="1", sim_serial_number="1", application_id=11,
                                    tx_bytes=11, rx_bytes=0, network_type=1, date=datetime.now())]

        device1.application_traffic_events = events

        # carriers
        carrier1 = Carrier(name="test_carrier_1")

        carrier1.sims = [sim1]

        for app in apps:
            db.session.add(app)
        db.session.add(carrier1)
        db.session.commit()

    def test_application_report_generation(self):
        with application.app_context():
            application_report = app_report(min_date=datetime.now() + timedelta(days=-1))
            application_report_expected = {
                1: {
                    "MOBILE": {
                        "ALL": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "513.0", "total_bytes": "513"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "258.0", "total_bytes": "258"},
                            3: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "131.0", "total_bytes": "131"},
                            4: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "68.0", "total_bytes": "68"},
                            5: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "37.0", "total_bytes": "37"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "22.0", "total_bytes": "22"},
                            7: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "15.0", "total_bytes": "15"},
                            8: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "12.0", "total_bytes": "12"},
                            9: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"},
                            10: {"app_name": "app11", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"}},
                        "UPLOAD": {
                            1: {"app_name": "app11", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"},
                            2: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "10.0", "total_bytes": "10"},
                            3: {"app_name": "app9", "total_devices": 1, "bytes_per_user": "9.0", "total_bytes": "9"},
                            4: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "8.0", "total_bytes": "8"},
                            5: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "7.0", "total_bytes": "7"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "6.0", "total_bytes": "6"},
                            7: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "5.0", "total_bytes": "5"},
                            8: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"},
                            9: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "3.0", "total_bytes": "3"},
                            10: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "512.0", "total_bytes": "512"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "256.0", "total_bytes": "256"},
                            3: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "128.0", "total_bytes": "128"},
                            4: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "64.0", "total_bytes": "64"},
                            5: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "32.0", "total_bytes": "32"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "16.0", "total_bytes": "16"},
                            7: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "8.0", "total_bytes": "8"},
                            8: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"},
                            9: {"app_name": "app9", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            10: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}
                    },
                    "WIFI": {"ALL": {}, "UPLOAD": {}, "DOWNLOAD": {}}},
                "ALL_CARRIERS": {
                    "MOBILE": {
                        "ALL": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "513.0", "total_bytes": "513"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "258.0", "total_bytes": "258"},
                            3: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "131.0", "total_bytes": "131"},
                            4: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "68.0", "total_bytes": "68"},
                            5: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "37.0", "total_bytes": "37"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "22.0", "total_bytes": "22"},
                            7: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "15.0", "total_bytes": "15"},
                            8: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "12.0", "total_bytes": "12"},
                            9: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"},
                            10: {"app_name": "app11", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"}},
                        "UPLOAD": {
                            1: {"app_name": "app11", "total_devices": 1, "bytes_per_user": "11.0", "total_bytes": "11"},
                            2: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "10.0", "total_bytes": "10"},
                            3: {"app_name": "app9", "total_devices": 1, "bytes_per_user": "9.0", "total_bytes": "9"},
                            4: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "8.0", "total_bytes": "8"},
                            5: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "7.0", "total_bytes": "7"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "6.0", "total_bytes": "6"},
                            7: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "5.0", "total_bytes": "5"},
                            8: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"},
                            9: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "3.0", "total_bytes": "3"},
                            10: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"}},
                        "DOWNLOAD": {
                            1: {"app_name": "app1", "total_devices": 1, "bytes_per_user": "512.0", "total_bytes": "512"},
                            2: {"app_name": "app2", "total_devices": 1, "bytes_per_user": "256.0", "total_bytes": "256"},
                            3: {"app_name": "app3", "total_devices": 1, "bytes_per_user": "128.0", "total_bytes": "128"},
                            4: {"app_name": "app4", "total_devices": 1, "bytes_per_user": "64.0", "total_bytes": "64"},
                            5: {"app_name": "app5", "total_devices": 1, "bytes_per_user": "32.0", "total_bytes": "32"},
                            6: {"app_name": "app6", "total_devices": 1, "bytes_per_user": "16.0", "total_bytes": "16"},
                            7: {"app_name": "app7", "total_devices": 1, "bytes_per_user": "8.0", "total_bytes": "8"},
                            8: {"app_name": "app8", "total_devices": 1, "bytes_per_user": "4.0", "total_bytes": "4"},
                            9: {"app_name": "app9", "total_devices": 1, "bytes_per_user": "2.0", "total_bytes": "2"},
                            10: {"app_name": "app10", "total_devices": 1, "bytes_per_user": "1.0", "total_bytes": "1"}}
                    },
                    "WIFI": {"ALL": {}, "UPLOAD": {}, "DOWNLOAD": {}}}
            }
            self.assertEqual(len(application_report), 2)
            carriers = [1, "ALL_CARRIERS"]
            for carrier in carriers:
                self.assertIn(carrier, application_report)
                self.assertIn("WIFI", application_report[carrier])
                self.assertDictEqual(application_report[carrier]["WIFI"],
                                     application_report_expected[carrier]["WIFI"],
                                     msg="Wifi report not empty for carrier " + str(carrier))
                self.assertIn("MOBILE", application_report[carrier])
                network_type = "MOBILE"
                self.assertIn(network_type, application_report[carrier])
                connection_modes = ["ALL", "UPLOAD", "DOWNLOAD"]
                for connection_mode in connection_modes:
                    self.assertIn(connection_mode, application_report[carrier][network_type])
                    self.assertEqual(len(application_report[carrier][network_type][connection_mode]), 10)
                    for i in range(1, 11):
                        self.assertIn(i, application_report[carrier][network_type][connection_mode])
                        fail_message = "Test failed for Carrier: %s, Network Type: %s, Mode: %s, index: %s" % \
                                       (str(carrier), network_type, connection_mode, str(i))
                        self.assertDictEqual(application_report[carrier][network_type][connection_mode][i],
                                             application_report_expected[carrier][network_type][connection_mode][i],
                                             msg=fail_message)




