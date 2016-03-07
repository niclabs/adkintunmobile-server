from datetime import datetime

from app import app
from . import base_test_case


class APITestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''
    def test_registration(self):
        from app.models.sim import Sim
        with app.app_context():
            date = datetime.now().date()
            request = self.app.post('/api/registration')
            assert request.status_code == 201
            Sim = Sim.query.all()
            assert len(Sim) == 1
            assert Sim[0].serial_number == 1
            assert Sim[0].creation_date == date
            #TODO: Cambiar última comprobación por una diferencia de tiempo en vez de la fecha