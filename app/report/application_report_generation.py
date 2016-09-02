from datetime import datetime

from sqlalchemy import text

from app import db
from app.report.reports_generation import BASE_DIRECTORY_REPORTS, save_json_report_to_file

APP_REPORT_DIRECTORY = BASE_DIRECTORY_REPORTS + 'apps_reports'


def generate_json_app_reports(init_date, last_date):
    """
    Calculate the app report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    report = app_report(init_date, last_date)

    save_json_report_to_file(report, init_date.year, init_date.month, APP_REPORT_DIRECTORY,
                             "apps_report_")


# app report
def app_report(min_date=datetime(2015, 1, 1),
               max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    from app.models.carrier import Carrier
    from app.models.application import Application


    carriers_id = [ c.id for c in Carrier.query.all()]
    carriers_id.append("ALL_CARRIERS")
    network_type = {"MOBILE": 1, "WIFI": 6}
    connection_mode = {"UPLOAD": "tx_bytes", "DOWNLOAD": "rx_bytes", "ALL":""}
    final = {}

    #carrier analysis
    for c in carriers_id:
        final[c] = {}

        if c=="ALL_CARRIERS":
            carrier_stmt = ""
        else:
            carrier_stmt = "sims.serial_number = events.sim_serial_number AND" \
                           " sims.carrier_id = :carrier_id AND"


        for type, value in network_type.items():
            final[c][type] = {}
            for mode, name in connection_mode.items():
                final[c][type][mode] = {}



                if mode=="ALL":
                    connection_stmt = "SUM(traffic_events.tx_bytes + traffic_events.rx_bytes) AS bytes,"
                else:
                    connection_stmt = "SUM(traffic_events." + name + ") AS bytes,"

                stmt = text(
                    """
                    SELECT
                      """+connection_stmt+"""
                      applications.package_name
                    FROM
                      public.traffic_events,
                      public.events,
                      public.applications,
                      public.application_traffic_events,
                      public.sims
                    WHERE
                      events.id = traffic_events.id AND
                      applications.id = application_traffic_events.application_id AND
                      application_traffic_events.id = traffic_events.id AND
                      """+carrier_stmt+"""
                      traffic_events.network_type = :network_type AND
                      events.date BETWEEN :min_date AND :max_date
                    GROUP BY applications.package_name
                    ORDER BY bytes DESC
                    LIMIT :number_app;
                    """)

                result = db.session.query(Application.package_name).add_columns("bytes").from_statement(stmt).params(
                    min_date=min_date, max_date=max_date, network_type=value, carrier_id=c, number_app=10)
                count = 1
                for row in result.all():
                    final[c][type][mode][count] = dict(package_name=row[0], bytes=str(row[1]))
                    count = count + 1


    return final
