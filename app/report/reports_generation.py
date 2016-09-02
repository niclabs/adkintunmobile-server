import os
from datetime import datetime, timedelta

from flask import json

BASE_DIRECTORY_REPORTS = 'app/static/reports/'


def monthly_reports_generation():
    from app.report.general_report_generation import generate_json_general_reports
    from app.report.antenna_network_report_generation import generate_json_network_reports
    from app.report.antenna_signal_report_generation import generate_json_signal_reports
    from app.report.application_report_generation import generate_json_app_reports

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

    generate_json_general_reports(init_date, last_date)
    generate_json_network_reports(init_date, last_date)
    generate_json_signal_reports(init_date, last_date)
    generate_json_app_reports(init_date, last_date)


def save_json_report_to_file(json_data: dict, year: int, month: int, folder: str, name: str):
    """
    Save data from a json to a file in the reports folder
    :param json_data: Json data
    :param year: year of the report
    :param month: month of the report
    :param folder: folder to store the json file
    :param name: name of the json file
    :return: None
    """

    file_folder = folder + "/" + str(year) + "/"
    file_name = name + str(month) + "_" + str(year) + ".json"

    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file_folder + file_name, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=False)
