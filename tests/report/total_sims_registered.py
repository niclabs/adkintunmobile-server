from app import app, db
from app.models.sim import Sim
from app.report.report import totalSimsRegistered
from tests import base_test_case


class TotalSimsRegisteredTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # sims
        sim1 = Sim(serial_number="123")
        sim2 = Sim(serial_number="456")
        sim3 = Sim(serial_number="789")

        db.session.add(sim1)
        db.session.add(sim2)
        db.session.add(sim3)
        db.session.commit()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_two_devices(self):
        with app.app_context():
            total_sims = totalSimsRegistered()
            assert total_sims == 3
