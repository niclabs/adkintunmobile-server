from datetime import datetime

from app.report.report_generation import generate_json_general_reports
from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler():
    pass
    scheduler = BackgroundScheduler()
    start_date = get_first_day()
    scheduler.add_job(generate_json_general_reports(), 'interval', id="procesamiento mensual", replace_existing=True,
                      months=1,
                      start_date=get_first_day())
    scheduler.start()


def get_first_day():
    return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
