from app import application
from app.models.carrier import Carrier
from tests import base_test_case
from tests.populate_db.populate_methods import populate_standard_test


class InitialdataTestCase(base_test_case.BaseTestCase):
    def populate(self):
        populate_standard_test()

    def test_save_carriers(self):
        with application.app_context():
            carriers = Carrier.query.all()
            carriersFiltered = Carrier.query.filter(Carrier.mnc == 9).all()

            assert len(carriers) == 14
            assert len(carriersFiltered) == 1
            assert carriersFiltered[0].name == "WOM"
