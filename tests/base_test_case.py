import unittest

from app import app, db
from app.models.sim import Sim
from app.models.carrier import Carrier
from dateutil.parser import parse


class BaseTestCase(unittest.TestCase):
    __test__ = False

    sim = {
        'creation_date': '04/02/2016',
    }

    def setUp(self, populate=True):
        # Load testing configuration
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

        # Initialize the request context
        self.context = app.test_request_context()
        self.context.push()

        # load data
        if (populate):
            self.populate()

    def populate(self):
        '''
        Populate the model with test data
        '''
        # Create the default sim
        carrier = Carrier("test", 1, 456)
        sim = Sim(creation_date=parse(self.sim.get('creation_date')), serial_number=1234, carrier=carrier)
        try:
            db.session.add(sim)
            db.session.add(carrier)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def tearDown(self):
        db.drop_all(bind=None)
        self.context.pop()
