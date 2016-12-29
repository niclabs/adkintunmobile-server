from datetime import datetime

from app import application
from tests.populate_db.populate_methods import populate_standard_test
from app.models.speedtests.connectivity_test_report import ConnectivityTestReport
from config import AppTokens
from tests import base_test_case
from tests.speedtest.speedtest_json import reports_json


class SaveConnectivityTestReports(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        populate_standard_test()

    # Saving events test: 1 connectivity event
    def test_save_connectivity_event(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=reports_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201
            connectivity_test_reports = ConnectivityTestReport.query.all()
            assert len(connectivity_test_reports) == 1

            connectivity_test_report = connectivity_test_reports[0]


