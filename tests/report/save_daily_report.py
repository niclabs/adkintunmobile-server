from datetime import datetime, timedelta

from app import app, db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.daily_report import DailyReport
from app.models.sim import Sim
from app.report.report_generation import total_device_for_carrier
from tests import base_test_case


class SaveDailyTestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def populate(self):
        # devices
        device1 = Device(device_id="1", creation_date=datetime.now() + timedelta(days=-2))
        device2 = Device(device_id="2", creation_date=datetime.now())
        device3 = Device(device_id="3", creation_date=datetime.now())
        device4 = Device(device_id="4", creation_date=datetime.now())

        # sims
        sim1 = Sim(serial_number="123")
        sim2 = Sim(serial_number="456")
        sim3 = Sim(serial_number="789")

        sim1.devices.append(device1)
        sim1.devices.append(device2)
        sim2.devices.append(device3)
        sim3.devices.append(device4)

        # carriers
        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")

        carrier1.sims.append(sim1)
        carrier1.sims.append(sim2)
        carrier2.sims.append(sim3)

        report = DailyReport()
        report.carrier = carrier1


        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.add(report)


        db.session.commit()

    # test de guardado de eventos: 1 wifi traffic event y 2 state change event
    def test_two_carrier(self):
        with app.app_context():
            reports = DailyReport.query.all()
            carrier = reports[0].carrier
            assert len(reports) == 1
            assert carrier.name == "test_carrier_1"
