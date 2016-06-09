from datetime import datetime, timedelta

from app import app, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.sim import Sim
from app.report.report_generation import total_device_for_carrier, total_sims_for_carrier
from tests import base_test_case


class TotalDevicesForCarrierReportedTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # sims
        sim1 = Sim(serial_number="123", creation_date=datetime.now() + timedelta(days=-2))
        sim2 = Sim(serial_number="456", creation_date=datetime.now())
        sim3 = Sim(serial_number="789", creation_date=datetime.now())

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.sims.append(sim1)
        carrier1.sims.append(sim2)
        carrier2.sims.append(sim3)

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_two_carrier(self):
        with app.app_context():
            sims_for_carrier = total_sims_for_carrier()
            assert len(sims_for_carrier) == 2

            assert sims_for_carrier[0].Carrier.name == "test_carrier_1"
            assert sims_for_carrier[1].Carrier.name == "test_carrier_2"
            assert sims_for_carrier[0].sims_count == 2
            assert sims_for_carrier[1].sims_count == 1

    def test_date_filter(self):
        with app.app_context():
            sims_for_carrier = total_sims_for_carrier(min_date=(datetime.now() + timedelta(days=-1)))
            assert len(sims_for_carrier) == 2

            assert sims_for_carrier[0].Carrier.name == "test_carrier_1"
            assert sims_for_carrier[1].Carrier.name == "test_carrier_2"
            assert sims_for_carrier[0].sims_count == 1
            assert sims_for_carrier[1].sims_count == 1