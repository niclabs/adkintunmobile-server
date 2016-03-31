from datetime import datetime

from app import app, db
from dateutil.parser import parse
from tests import base_test_case


class TestRegistration(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''

    def test_registration(self):
        from app.models.sim import Sim
        from app.models.device import Device

        with app.app_context():
            date = datetime.now().date()
            request = self.app.post('/api/registration', data=dict(
                    serial_number=123,
                    carrier_id=456,
                    brand="brand test",
                    board="board test",
                    build_id="build id test",
                    device="device test",
                    hardware="hardware test",
                    manufacturer="manufacturer test",
                    model="model test",
                    release="release test",
                    release_type="release type test",
                    product="product test",
                    sdk=4,
                    device_id=8000000000000000000
            ))
            assert request.status_code == 201
            # assert SIM
            sim = Sim.query.all()
            assert len(sim) == 1
            assert sim[0].serial_number == 123
            assert sim[0].creation_date == date

            # assert Device
            devices = Device.query.all()
            assert len(devices) == 1
            device = devices[0]
            assert device.brand == "brand test"
            assert device.board == "board test"
            assert device.build_id == "build id test"
            assert device.device == "device test"
            assert device.hardware == "hardware test"
            assert device.manufacturer == "manufacturer test"
            assert device.model == "model test"
            assert device.release == "release test"
            assert device.release_type == "release type test"
            assert device.product == "product test"
            assert device.sdk == 4
            assert device.device_id == 8000000000000000000

            # assert relationship device-sim
            assert sim[0].devices.count() == 1
            assert sim[0].devices[0].device_id == device.device_id

            # assert relationship carrier-sim (no podemos garantizar que sólo exista una)
            carrier = sim[0].carrier
            assert carrier.sims.filter(Sim.carrier_id == sim[0].carrier_id).first()


            # TODO: Cambiar última comprobación por una diferencia de tiempo en vez de la fecha

    sim = {
        'creation_date': '04/02/2016',
    }

    def populate(self):
        '''
        Populate the model with test data
        '''
        from app.models.carrier import Carrier
        from app.models.sim import Sim
        # Create the default sim
        carrier = Carrier("test", 1, 456)
        sim = Sim(creation_date=parse(self.sim.get('creation_date')), serial_number=1234)
        try:
            db.session.add(carrier)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
