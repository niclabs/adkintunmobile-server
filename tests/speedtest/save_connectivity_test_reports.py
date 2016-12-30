from datetime import datetime

from app import application
from app.models.speedtests.connectivity_test_report import ConnectivityTestReport
from config import AppTokens
from tests import base_test_case
from tests.populate_db.populate_methods import populate_standard_test
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

    # Saving 3 test report: 1 connectivity test report
    def test_save_connectivity_test_report(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=reports_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201
            connectivity_test_reports = ConnectivityTestReport.query.all()
            assert len(connectivity_test_reports) == 1

            connectivity_test_report = connectivity_test_reports[0]

            assert not connectivity_test_report.dispatched
            assert connectivity_test_report.date.date() == datetime.fromtimestamp(1482341840760 / 1000).date()

            # test network interface
            from app.models.speedtests.network_interface import NetworkInterface

            assert len(NetworkInterface.query.all()) == 3
            ni = NetworkInterface.query.filter(NetworkInterface.network_type==1).first()

            assert ni.id == connectivity_test_report.network_interface_id
            assert ni.active_interface == 2
            assert ni.bssid == "00:17:5a:1e:70:80"
            assert ni.gsm_cid == 0
            assert ni.gsm_lac == 0
            assert ni.ssid == "'niclabs'"

            # test sites results
            from app.models.speedtests.site_result import SiteResult
            assert len(connectivity_test_report.sites_results.all()) == len(SiteResult.query.all())

