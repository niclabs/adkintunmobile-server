from tests import base_test_case
from manage import init_db
from app.models.carrier import Carrier


class InitialDataTestCase(base_test_case.BaseTestCase):
    def populate(self):
        pass

    def test_save_carriers(self):
        init_db()
        carriers = Carrier.query.all()
        self.assertEqual(len(carriers), 0)
        pass
