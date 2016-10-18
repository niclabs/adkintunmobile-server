import os
from datetime import datetime, timedelta

from flask import json

BASE_DIRECTORY_REPORTS = 'app/static/reports/'


def monthly_reports_generation(month=None, year=None):
    """
    Generate reports for a month of a particular year. If month and year are not added, it generate the report of the last month
    :param month: Month of the report
    :param year: year of the report
    :return: None
    """
    from app.report.general_report_generation import generate_json_general_reports
    from app.report.antenna_network_report_generation import generate_json_network_reports
    from app.report.antenna_signal_report_generation import generate_json_signal_reports
    from app.report.application_report_generation import generate_json_app_reports

    # get month for the report, not added month or year
    if not month or not year:
        final_month = datetime.now().month
        final_year = datetime.now().year
        month_new_report = final_month - 1
        year_new_report = final_year
        if month_new_report == 0:
            month_new_report = 12
            year_new_report = year_new_report - 1
    else:
        year_new_report = int(year)
        month_new_report = int(month)
        final_month = month_new_report + 1
        final_year = year_new_report
        if final_month == 13:
            final_month = 1
            final_year = year_new_report + 1

    # select limit dates of the selected month
    init_date = datetime(year=year_new_report, month=month_new_report, day=1)
    last_date = datetime(year=final_year, month=final_month, day=1, hour=23, minute=59, second=59) - timedelta(days=1)

    generate_json_general_reports(init_date, last_date)
    generate_json_network_reports(init_date, last_date)
    generate_json_signal_reports(init_date, last_date)
    generate_json_app_reports(init_date, last_date)


def save_json_report_to_file(json_data: dict, year: int, month: int, name: str):
    """
    Save data from a json to a file in the reports folder
    :param json_data: Json data
    :param year: year of the report
    :param month: month of the report
    :param name: name of the json file
    :return: None
    """

    file_folder = BASE_DIRECTORY_REPORTS + "/" + str(year) + "/" + str(month) + "/"
    file_name = name + str(month) + "_" + str(year) + ".json"

    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file_folder + file_name, "w") as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=False)
