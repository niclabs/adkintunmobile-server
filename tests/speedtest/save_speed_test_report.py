from datetime import datetime

from app import application
from app.models.speedtests.speed_test_report import SpeedTestReport
from config import AppTokens
from tests import base_test_case
from tests.populate_db.populate_methods import populate_standard_test
from tests.speedtest.speedtest_json import reports_json


class SaveSpeedTestReports(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        populate_standard_test()

    # Saving 3 test report: 1 speed test report
    def test_save_speed_test_report(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=reports_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201
            speed_test_reports = SpeedTestReport.query.all()
            assert len(speed_test_reports) == 1

            speed_test_report = speed_test_reports[0]

            assert not speed_test_report.dispatched
            assert speed_test_report.download_size == 1000000
            assert speed_test_report.download_speed == 9965900.0
            assert speed_test_report.elapsed_download_time == 838
            assert speed_test_report.elapsed_upload_time == 798
            assert speed_test_report.host == "http://blasco.duckdns.org"
            assert speed_test_report.upload_size == 1000000
            assert speed_test_report.upload_speed == 9854887.0

            assert speed_test_report.date.date() == datetime.fromtimestamp(1482341701645 / 1000).date()

            # test network interface
            from app.models.speedtests.network_interface import NetworkInterface

            #self.assertEqual(len(NetworkInterface.query.all()), 3)
            assert len(NetworkInterface.query.all()) == 3
            ni = NetworkInterface.query.filter(NetworkInterface.network_type == 3).first()

            assert ni.id == speed_test_report.network_interface_id
            assert ni.active_interface == 2
            assert ni.bssid == "00:17:5a:1e:70:80"
            assert ni.gsm_cid == 0
            assert ni.gsm_lac == 0
            assert ni.ssid == "'niclabs'"
