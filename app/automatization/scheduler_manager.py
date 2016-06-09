from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.report.report_generation import generate_report


def start_scheduler():
    scheduler = BackgroundScheduler()
    start_date=today_init_time()
    scheduler.add_job(generate_report, 'interval', id="procesamiento diario", replace_existing=True, days=1,
                      start_date=today_init_time())
    print("Reportes seteados a las "+str(start_date))
    scheduler.start()

def today_init_time():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

