from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.data.antennas_geolocalization import update_antennas_localization
from app.report.reports_generation import monthly_reports_generation


def start_scheduler():
    scheduler = BackgroundScheduler()
    start_date = get_first_day()
    scheduler.add_job(monthly_reports_generation, trigger="cron", id="Monthly reports generation",
                      replace_existing=True,
                      day="1", hour="0", minute="0", start_date=start_date)
    scheduler.add_job(update_antennas_localization, kwargs={"max_number_of_queries": 1000}, trigger="cron",
                      id="Antennas geolocalization", replace_existing=True, hour=3, minute=0)
    scheduler.start()


def get_first_day():
    return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Start scheduler with automatic report generation and antenna geolocalization
start_scheduler()