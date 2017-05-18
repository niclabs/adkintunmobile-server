from datetime import datetime, timedelta

from app import application, db
from app.models.sim import Sim
from app.report.general_report_generation import total_sims_registered
from tests import base_test_case


class TotalSimsRegisteredTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # sims
        sim1 = Sim(serial_number="123", creation_date=datetime.now() + timedelta(days=-2))
        sim2 = Sim(serial_number="456", creation_date=datetime.now())
        sim3 = Sim(serial_number="789", creation_date=datetime.now())

        db.session.add(sim1)
        db.session.add(sim2)
        db.session.add(sim3)
        db.session.commit()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_two_devices(self):
        with application.app_context():
            total_sims = total_sims_registered()
            self.assertEqual(total_sims, 3)

    def test_date_filter(self):
        with application.app_context():
            total_sims = total_sims_registered(min_date=(datetime.now() + timedelta(days=-1)))
            self.assertEqual(total_sims, 2)
