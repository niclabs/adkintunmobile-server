from datetime import datetime, timedelta

from app import application, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.gsm_event import GsmEvent
from app.models.antenna import Antenna
from app.report.antenna_network_report_generation import network_report_for_carrier
from tests import base_test_case


class Antenna4GReportTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        #antennas
        antenna1 = Antenna(carrier_id=1)
        antenna2 = Antenna(carrier_id=1)
        antenna3 = Antenna(carrier_id=2)
        antenna4 = Antenna(carrier_id=2)

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.antennas.append(antenna1)
        carrier2.antennas.append(antenna2)
        carrier2.antennas.append(antenna3)

        # devices

        device1 = Device(device_id="1")
        device2 = Device(device_id="2")
        device3 = Device(device_id="3")

        # GSM events
        event1 = GsmEvent(date=datetime.now() + timedelta(days=-2), antenna_id=1,
                          network_type=14, signal_strength_size=1)
        event2 = GsmEvent(date=datetime.now(), antenna_id=2, network_type=14, signal_strength_size=1)
        event3 = GsmEvent(date=datetime.now(), antenna_id=2, network_type=15, signal_strength_size=1)
        event4 = GsmEvent(date=datetime.now(), antenna_id=3, network_type=14, signal_strength_size=2)
        event5 = GsmEvent(date=datetime.now(), antenna_id=3, network_type=15, signal_strength_size=1)
        event6 = GsmEvent(date=datetime.now(), antenna_id=4, network_type=11, signal_strength_size=1)

        device1.gsm_events = [event1, event2, event3]
        device2.gsm_events = [event4, event5]
        device3.gsm_events = [event6]

        carrier1.gsm_events = [event1, event2, event3]
        carrier2.gsm_events = [event4, event5, event6]

        db.session.add(device1)
        db.session.add(device2)
        db.session.add(device3)
        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_network_report_uses_all_antennas(self):
        with application.app_context():
            antenna_network_report = network_report_for_carrier()
            self.assertEqual(len(antenna_network_report), 4)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 1, '4g_events': 1, "non_4g_events": 0},
                {'carrier_id': 1, 'antenna_id': 2, '4g_events': 1, "non_4g_events": 1},
                {'carrier_id': 2, 'antenna_id': 3, '4g_events': 2, "non_4g_events": 1}
            ]
            self.assertEqual(antenna_network_report, antenna_network_report_expected)

    def test_network_report_filters_events_by_date(self):
        with application.app_context():
            antenna_network_report = network_report_for_carrier(min_date=datetime.now() + timedelta(days=-1))
            self.assertEqual(len(antenna_network_report), 3)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id'], d['network_type']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 2, '4g_events': 1, "non_4g_events": 1},
                {'carrier_id': 2, 'antenna_id': 3, '4g_events': 2, "non_4g_events": 1}]
            self.assertEqual(antenna_network_report, antenna_network_report_expected)
