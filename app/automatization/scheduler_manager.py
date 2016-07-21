from datetime import datetime

from app.report.reports_generation import monthly_reports_generation
from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler():
    scheduler = BackgroundScheduler()
    start_date = get_first_day()
    scheduler.add_job(monthly_reports_generation, "cron", id="procesamiento mensual", replace_existing=True,
                      day="1", hour="0", minute="0", start_date=start_date)
    scheduler.start()


def get_first_day():
    return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
