from . import base_test_case


class APITestCase(base_test_case.BaseTestCase):
    '''
    Unit tests for the API
    '''
    def test_registration(self):
        request = self.app.post('/api/registration')
        assert request.status_code == 201
