from datetime import datetime

BASE_DIRECTORY_REPORTS = 'app/static/reports/'
GENERAL_REPORT_DIRECTORY = BASE_DIRECTORY_REPORTS + 'signal_reports'


# Signal strength mean by antenna
def signal_strength_mean_for_antenna(min_date=datetime(2015, 1, 1),
                                     max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    pass
