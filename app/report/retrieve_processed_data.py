from datetime import datetime

from app import db
from sqlalchemy import func, and_


# Total de equipos que han entregado datos
def get_stored_data(min_date=datetime(2015, 1, 1),
                    max_date=datetime.now()):
    from app.models.daily_report import DailyReport

    if not min_date or min_date < datetime(2015, 1, 1):
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    all_data = db.session.query(func.sum(DailyReport.total_devices).label('total_devices'),
                                func.sum(DailyReport.total_sims).label('total_sims'),
                                func.sum(DailyReport.total_events).label('total_events'),
                                func.sum(DailyReport.devices_none).label('devices_none'),
                                func.sum(DailyReport.devices_entel).label('devices_entel'),
                                func.sum(DailyReport.devices_movistar).label('devices_movistar'),
                                func.sum(DailyReport.devices_claro).label('devices_claro'),
                                func.sum(DailyReport.devices_nextel).label('devices_nextel'),
                                func.sum(DailyReport.devices_wom).label('devices_wom'),
                                func.sum(DailyReport.devices_tds).label('devices_tds'),
                                func.sum(DailyReport.devices_vtrm).label('devices_vtrm'),
                                func.sum(DailyReport.devices_ccwm).label('devices_ccwm'),
                                func.sum(DailyReport.devices_virginm).label('devices_virginm'),
                                func.sum(DailyReport.devices_will).label('devices_will'),
                                func.sum(DailyReport.devices_celupago).label('devices_celupago'),
                                func.sum(DailyReport.devices_netline).label('devices_netline'),
                                func.sum(DailyReport.sims_none).label('sims_none'),
                                func.sum(DailyReport.sims_entel).label('sims_entel'),
                                func.sum(DailyReport.sims_movistar).label('sims_movistar'),
                                func.sum(DailyReport.sims_claro).label('sims_claro'),
                                func.sum(DailyReport.sims_nextel).label('sims_nextel'),
                                func.sum(DailyReport.sims_wom).label('sims_wom'),
                                func.sum(DailyReport.sims_tds).label('sims_tds'),
                                func.sum(DailyReport.sims_vtrm).label('sims_vtrm'),
                                func.sum(DailyReport.sims_ccwm).label('sims_ccwm'),
                                func.sum(DailyReport.sims_virginm).label('sims_virginm'),
                                func.sum(DailyReport.sims_will).label('sims_will'),
                                func.sum(DailyReport.sims_celupago).label('sims_celupago'),
                                func.sum(DailyReport.sims_netline).label('sims_netline'),
                                func.sum(DailyReport.events_none).label('events_none'),
                                func.sum(DailyReport.events_entel).label('events_entel'),
                                func.sum(DailyReport.events_movistar).label('events_movistar'),
                                func.sum(DailyReport.events_claro).label('events_claro'),
                                func.sum(DailyReport.events_nextel).label('events_nextel'),
                                func.sum(DailyReport.events_wom).label('events_wom'),
                                func.sum(DailyReport.events_tds).label('events_tds'),
                                func.sum(DailyReport.events_vtrm).label('events_vtrm'),
                                func.sum(DailyReport.events_ccwm).label('events_ccwm'),
                                func.sum(DailyReport.events_virginm).label('events_virginm'),
                                func.sum(DailyReport.events_will).label('events_will'),
                                func.sum(DailyReport.events_celupago).label('events_celupago'),
                                func.sum(DailyReport.events_netline).label('events_netline')). \
        filter(and_(DailyReport.init_date >= min_date, DailyReport.final_date <= max_date)).all()

    return all_data
