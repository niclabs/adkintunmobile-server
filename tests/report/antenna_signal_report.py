from datetime import datetime, timedelta

from app import application, db
from app.models.carrier import Carrier
from app.models.gsm_event import GsmEvent
from app.models.antenna import Antenna
from app.report.antenna_network_report_generation import network_report_for_carrier
from tests import base_test_case


class AntennaNetworkReportTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        #antennas
        antenna1 = Antenna(carrier_id=1)
        antenna2 = Antenna(carrier_id=2)
        antenna3 = Antenna(carrier_id=2)

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.antennas.append(antenna1)
        carrier2.antennas.append(antenna2)
        carrier2.antennas.append(antenna3)

        # GSM events
        event1 = GsmEvent(date=datetime.now() + timedelta(days=-2), antenna_id=1, network_type=1)
        event2 = GsmEvent(date=datetime.now(), antenna_id=1, network_type=2)
        event3 = GsmEvent(date=datetime.now(), antenna_id=2, network_type=1)
        event4 = GsmEvent(date=datetime.now(), antenna_id=3, network_type=1)
        event5 = GsmEvent(date=datetime.now(), antenna_id=3, network_type=1)

        carrier1.gsm_events = [event1, event2]
        carrier2.gsm_events = [event3, event4, event5]

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_network_report_uses_all_antennas(self):
        with application.app_context():
            antenna_network_report = network_report_for_carrier()
            self.assertEqual(len(antenna_network_report), 4)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id'], d['network_type']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 2, 'antenna_id': 2, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 2, 'antenna_id': 3, 'observations': 2, 'signal_mean': 0}]
            self.assertEqual(antenna_network_report, antenna_network_report_expected)

    def test_network_report_filters_events_by_date(self):
        with application.app_context():
            antenna_network_report = network_report_for_carrier(min_date=datetime.now() + timedelta(days=-1))
            self.assertEqual(len(antenna_network_report), 3)
            antenna_network_report.sort(key=lambda d: (d['carrier_id'], d['antenna_id'], d['network_type']))
            antenna_network_report_expected = [
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 1, 'antenna_id': 1, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 2, 'antenna_id': 2, 'observations': 1, 'signal_mean': 0},
                {'carrier_id': 2, 'antenna_id': 3, 'observations': 2, 'signal_mean': 0}]
            self.assertEqual(antenna_network_report, antenna_network_report_expected)