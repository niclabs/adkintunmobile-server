import unittest

from app import application, db


class BaseTestCase(unittest.TestCase):
    def tearDown(self):
        db.drop_all(bind=None)
        self.context.pop()

    def setUp(self, populate=True):
        # Load testing configuration
        application.config.from_object('config.TestingConfig')
        self.app = application.test_client()
        db.create_all()

        # Initialize the request context
        self.context = application.test_request_context()
        self.context.push()

        # load data
        if (populate):
            self.populate()
