from datetime import datetime, timedelta

import os
from app import db
from flask import json

GENERAL_REPORT_DIRECTORY = 'reports/general_reports'


def generate_json_general_reports():
    '''
    Calculate the report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    '''

    # get month for the report
    actual_month = datetime.now().month
    actual_year = datetime.now().year
    month_new_report = actual_month - 1
    year_new_report = actual_year
    if month_new_report == 0:
        month_new_report = 12
        year_new_report = year_new_report - 1

    # select limit dates of the selected month
    init_date = datetime(year=year_new_report, month=month_new_report, day=1)
    last_date = datetime(year=actual_year, month=actual_month, day=1, hour=23, minute=59, second=59) - timedelta(days=1)

    total_devices = total_devices_reported(init_date, last_date)
    total_sims = total_sims_registered(init_date, last_date)
    total_gsm = total_gsm_events(init_date, last_date)
    total_device_carrier = total_device_for_carrier(init_date, last_date)
    total_sims_carrier = total_sims_for_carrier(init_date, last_date)
    total_gsm_carrier = total_gsm_events_for_carrier(init_date, last_date)

    final_json = {"total_sims": total_sims, "total_devices": total_devices, "total_gsm": total_gsm,
                  "total_gsm_carrier": serialize_pairs(total_gsm_carrier),
                  "total_sims_carrier": serialize_pairs(total_sims_carrier),
                  "total_device_carrier": serialize_pairs(total_device_carrier)}

    save_json_report_to_file(final_json, year_new_report, month_new_report, GENERAL_REPORT_DIRECTORY, "general_report_")


def save_json_report_to_file(json_data: dict, year: int, month: int, folder: str, name: str):
    '''

    Save data from a json to a file in the reports folder
    :param json_data: Json data        
    :param year: year of the report
    :param month: month of the report
    :param folder: folder to store the json file
    :param name: name of the json file
    :return: None
    '''
    file_folder = folder + '/' + str(year) + '/'
    file_name = name + str(month) + '_' + str(year) + '.json'

    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file_folder + file_name, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)


# Total de equipos que han entregado datos
def total_devices_reported(min_date=datetime(2015, 1, 1),
                           max_date=None):
    from app.models.device import Device

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Device.query.filter(Device.events != None, Device.creation_date.between(min_date, max_date)).count()


# Total de sims registradas
def total_sims_registered(min_date=datetime(2015, 1, 1),
                          max_date=None):
    from app.models.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Sim.query.filter(Sim.creation_date.between(min_date, max_date)).count()


# Total de mediciones de señal registradas (GSM)
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
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text('''
    SELECT consulta_1.id, count(id) as devices_count
    FROM
    (SELECT DISTINCT devices.device_id, carriers.id
    FROM devices
    JOIN devices_sims ON devices.device_id = devices_sims.device_id
    JOIN sims ON sims.serial_number = devices_sims.sim_id
    JOIN carriers on sims.carrier_id = carriers.id
    WHERE devices.creation_date BETWEEN :min_date AND :max_date) as consulta_1
    GROUP BY consulta_1.id''')

    result = db.session.query().add_columns('id', 'devices_count').from_statement(stmt).params(
            min_date=min_date, max_date=max_date)

    return result.all()


# Sims by company
def total_sims_for_carrier(min_date=datetime(2015, 1, 1),
                           max_date=None):
    from app.models.sim import Sim
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text('''
    SELECT carrier_id, count(*) AS sims_count
    FROM sims
    WHERE sims.creation_date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id''').columns(Sim.carrier_id)

    result = db.session.query(Sim.carrier_id).add_columns('sims_count').from_statement(stmt).params(
            min_date=min_date, max_date=max_date)

    return result.all()


# GSM events by telco
def total_gsm_events_for_carrier(min_date=datetime(2015, 1, 1),
                                 max_date=None):
    from app.models.gsm_event import GsmEvent
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text('''
    SELECT carrier_id, count(*) AS events_count
    FROM gsm_events
    JOIN events ON gsm_events.id = events.id
    JOIN sims ON events.sim_serial_number = sims.serial_number
    WHERE sims.creation_date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id ''').columns(GsmEvent.carrier_id)

    result = db.session.query(GsmEvent.carrier_id).add_columns('events_count').from_statement(stmt).params(
            min_date=min_date, max_date=max_date)

    return result.all()


def serialize_pairs(args):
    ans = {}
    for a in args:
        ans[str(a[0])] = a[1]
    return ans
