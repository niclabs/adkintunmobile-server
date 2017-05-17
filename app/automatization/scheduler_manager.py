from datetime import datetime

from uwsgidecorators import cron

from app import application
from app.data.antennas_geolocalization import update_antennas_localization
from app.report.reports_generation import monthly_reports_generation

MAX_NUMBER_OF_QUERIES = 40


# Job will be done the first day of every month
# @cron(0, 0, 1, -1, -1, target="mule")
# def reports_generation(num: int):
#     """
#     Job for generate diferents reports automatically
#     :param num: singal num
#     :return:
#     """
#     monthly_reports_generation()
#     application.logger.info(datetime.now().strftime("Reports has been generated. - %H:%M %d/%m/%Y"))


# Job will be done every hour, every day
@cron(0, -1, -1, -1, -1, target="mule")
def antennas_geolocalization(num: int):
    """
    Job for geolocalizate antennas every day
    :param num: signal num
    :return: None
    """
    ua = update_antennas_localization(MAX_NUMBER_OF_QUERIES)
    application.logger.info(
        "New geolocalized antennas: " + str(ua) + " antennas." + datetime.now().strftime(" - %H:%M %d/%m/%Y"))
