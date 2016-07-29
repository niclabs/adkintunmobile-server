from datetime import datetime

from app import db
from app.report.reports_generation import save_json_report_to_file
from sqlalchemy import text

BASE_DIRECTORY_REPORTS = "app/static/reports/"
GENERAL_REPORT_DIRECTORY = BASE_DIRECTORY_REPORTS + "general_reports"


def generate_json_general_reports(init_date, last_date):
    """
    Calculate the report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    total_devices = total_devices_registred(init_date, last_date)
    total_sims = total_sims_registered(init_date, last_date)
    total_gsm = total_gsm_events(init_date, last_date)
    total_device_carrier = total_device_for_carrier(init_date, last_date)
    total_sims_carrier = total_sims_for_carrier(init_date, last_date)
    total_gsm_carrier = total_gsm_events_for_carrier(init_date, last_date)

    final_json = {"total_sims": total_sims,
                  "total_devices": total_devices, "total_gsm": total_gsm,
                  "total_gsm_carrier": serialize_pairs(total_gsm_carrier),
                  "total_sims_carrier": serialize_pairs(total_sims_carrier),
                  "total_device_carrier": serialize_pairs(total_device_carrier)}

    save_json_report_to_file(final_json, init_date.year, init_date.month, GENERAL_REPORT_DIRECTORY,
                             "general_report_")  # Total devices registred


def total_devices_registred(min_date=datetime(2015, 1, 1),
                            max_date=None):
    from app.models.device import Device

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Device.query.filter(Device.events != None, Device.creation_date.between(min_date, max_date)).count()


# Total sim cards registred
def total_sims_registered(min_date=datetime(2015, 1, 1),
                          max_date=None):
    from app.models.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Sim.query.filter(Sim.creation_date.between(min_date, max_date)).count()


# Total signal meassurements registred (GSM events)
def total_gsm_events(min_date=datetime(2015, 1, 1),
                     max_date=None):
    from app.models.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return GsmEvent.query.filter(GsmEvent.date.between(min_date, max_date)).count()


# Devices by company
def total_device_for_carrier(min_date=datetime(2015, 1, 1),
                             max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT consulta_1.id, count(id) as devices_count
    FROM
    (SELECT DISTINCT devices.device_id, carriers.id
    FROM devices
    JOIN devices_sims ON devices.device_id = devices_sims.device_id
    JOIN sims ON sims.serial_number = devices_sims.sim_id
    JOIN carriers on sims.carrier_id = carriers.id
    WHERE devices.creation_date BETWEEN :min_date AND :max_date) as consulta_1
    GROUP BY consulta_1.id""")

    result = db.session.query().add_columns("id", "devices_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


# Sims by company
def total_sims_for_carrier(min_date=datetime(2015, 1, 1),
                           max_date=None):
    from app.models.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT sims.carrier_id, count(*) AS sims_count
    FROM sims
    WHERE sims.creation_date BETWEEN :min_date AND :max_date
    GROUP BY sims.carrier_id""")

    result = db.session.query(Sim.carrier_id).add_columns("sims_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


# GSM events by telco
def total_gsm_events_for_carrier(min_date=datetime(2015, 1, 1),
                                 max_date=None):
    from app.models.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT carrier_id, count(events.id) AS events_count
    FROM gsm_events
    JOIN events ON gsm_events.id = events.id
    JOIN sims ON events.sim_serial_number = sims.serial_number
    WHERE events.date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id """)

    result = db.session.query(GsmEvent.carrier_id).add_columns("events_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


def serialize_pairs(args):
    ans = {}
    for a in args:
        ans[str(a[0])] = a[1]
    return ans
