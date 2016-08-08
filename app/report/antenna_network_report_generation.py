from datetime import datetime

from sqlalchemy import text

from app import db
from app.models.antenna import Antenna
from app.models.sim import Sim
from app.models.telephony_observation_event import TelephonyObservationEvent
from app.report.reports_generation import save_json_report_to_file

BASE_DIRECTORY_REPORTS = 'app/static/reports/'
NETWORK_REPORT_DIRECTORY = BASE_DIRECTORY_REPORTS + 'network_reports'


def generate_json_network_reports(init_date, last_date):
    """
    Calculate the network report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    report = network_report_for_antenna(init_date, last_date)

    save_json_report_to_file(report, init_date.year, init_date.month, NETWORK_REPORT_DIRECTORY,
                             "network_report_")


# Signal strength mean by antenna
def network_report_for_antenna(min_date=datetime(2015, 1, 1),
                               max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT
        telephony_observation_events.network_type,
        antennas.id,
         sims.carrier_id,
        count(gsm_events.id) as size

    FROM
        public.antennas,
        public.gsm_events,
        public.events,
        public.telephony_observation_events,
        public.sims
    WHERE
        gsm_events.antenna_id = antennas.id AND
        gsm_events.id = telephony_observation_events.id AND
        events.id = gsm_events.id AND
        events.sim_serial_number = sims.serial_number AND
        events.date BETWEEN :min_date AND :max_date
    GROUP BY
        telephony_observation_events.network_type,
        antennas.id,
        sims.carrier_id;""")

    result = db.session.query( TelephonyObservationEvent.network_type, Antenna.id,
                              Sim.carrier_id).add_columns("size").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    final = [dict(network_type=row[0], antenna_id=row[1], carrier_id=row[2], size=row[3]) for row in
             result.all()]

    return final;
