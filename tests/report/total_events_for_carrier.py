from datetime import datetime, timedelta

from app import application, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.gsm_event import GsmEvent
from app.models.sim import Sim
from app.report.general_report_generation import total_gsm_events_for_carrier
from tests import base_test_case


class TotalGSMEventsForCarrierReportedTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # sims
        sim1 = Sim(serial_number="123")
        sim2 = Sim(serial_number="456")
        sim3 = Sim(serial_number="789")

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.sims.append(sim1)
        carrier1.sims.append(sim2)
        carrier2.sims.append(sim3)

        # GSM events
        event1 = GsmEvent(date=datetime.now() + timedelta(days=-2))
        event2 = GsmEvent(date=datetime.now())
        event3 = GsmEvent(date=datetime.now())
        event4 = GsmEvent(date=datetime.now())
        event5 = GsmEvent(date=datetime.now())

        sim1.gsm_events = [event1, event2]
        sim3.gsm_events = [event3, event4, event5]

        # Associate all events to carrier1 to show carrier_id is taken
        # the the sim and not the gsm_event
        carrier1.gsm_events = [event1, event2, event3, event4, event5]

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_two_carrier(self):
        with application.app_context():
            events_for_carrier = total_gsm_events_for_carrier()
            self.assertEqual(len(events_for_carrier), 2)

            self.assertEqual(events_for_carrier[0].carrier_id, 1)
            self.assertEqual(events_for_carrier[0].events_count, 2)
            self.assertEqual(events_for_carrier[1].carrier_id, 2)
            self.assertEqual(events_for_carrier[1].events_count, 3)


    def test_date_filter(self):
        with application.app_context():
            events_for_carrier = total_gsm_events_for_carrier(min_date=(datetime.now() + timedelta(days=-1)))
            self.assertEqual(len(events_for_carrier), 2)

            self.assertEqual(events_for_carrier[0].carrier_id, 1)
            self.assertEqual(events_for_carrier[0].events_count, 1)
            self.assertEqual(events_for_carrier[1].carrier_id, 2)
            self.assertEqual(events_for_carrier[1].events_count, 3)

