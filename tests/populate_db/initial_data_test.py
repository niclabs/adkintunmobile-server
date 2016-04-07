from app import app

from tests import base_test_case
from manage import populate
from app.models.carrier import Carrier


class InitialdataTestCase(base_test_case.BaseTestCase):
    def populate(self):
        pass

    def test_save_carriers(self):
        with app.app_context():
            populate()
            carriers = Carrier.query.all()
            carriersFiltered = Carrier.query.filter(Carrier.mnc == 9).all()

            assert len(carriers) == 12
            assert len(carriersFiltered) == 1
            assert carriersFiltered[0].name == "WOM"
