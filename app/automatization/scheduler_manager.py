from uwsgidecorators import cron

from app import app
from app.data.antennas_geolocalization import update_antennas_localization
from app.report.reports_generation import monthly_reports_generation

MAX_NUMBER_OF_QUERIES = 1000


@cron(0, 0, 1, -1, -1, target="mule")
def reports_generation(num):
    """
    Job for generate differents reports automatically
    :param num: singal num
    :return:
    """
    monthly_reports_generation()
    app.logger.info("Reports has been generated")


@cron(0, 3, -1, -1, -1, target="mule")
def antennas_geolocalization(num):
    """
    Job for geolocalizate antennas every day
    :param num: signal num
    :return: None
    """
    ua = update_antennas_localization(MAX_NUMBER_OF_QUERIES)
    app.logger.info("New geolocalized antennas: " + str(ua))
