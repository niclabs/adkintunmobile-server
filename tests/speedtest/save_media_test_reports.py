from datetime import datetime

from app import application
from app.models.speedtests.media_test_report import MediaTestReport
from config import AppTokens
from tests import base_test_case
from tests.populate_db.populate_methods import populate_standard_test
from tests.speedtest.speedtest_json import reports_json


class SaveMediaTestReports(base_test_case.BaseTestCase):
    """
    Unit tests for the API
    """

    def populate(self):
        """
        Populate the model with test data
        """
        populate_standard_test()

    # Saving 3 test report: 1 media test report
    def test_save_media_test_report(self):
        with application.app_context():
            token = list(AppTokens.tokens.keys())[0]
            request = self.app.post("/api/events", data=dict(
                events=reports_json
            ), headers={"Authorization": "token " + token})

            assert request.status_code == 201
            media_test_reports = MediaTestReport.query.all()
            assert len(media_test_reports) == 1

            media_test_report = media_test_reports[0]

            assert not media_test_report.dispatched
            assert media_test_report.video_id == "gPmbH8eCUj4"
            assert media_test_report.date.date() == datetime.fromtimestamp(1482341724349 / 1000).date()

            # test network interface
            from app.models.speedtests.network_interface import NetworkInterface

            assert len(NetworkInterface.query.all()) == 3
            ni = NetworkInterface.query.filter(NetworkInterface.network_type == 2).first()

            assert ni.id == media_test_report.network_interface_id
            assert ni.active_interface == 2
            assert ni.bssid == "00:17:5a:1e:70:80"
            assert ni.gsm_cid == 0
            assert ni.gsm_lac == 0
            assert ni.ssid == "'niclabs'"

            # test video results
            from app.models.speedtests.video_result import VideoResult
            assert len(media_test_report.video_results.all()) == len(VideoResult.query.all())
