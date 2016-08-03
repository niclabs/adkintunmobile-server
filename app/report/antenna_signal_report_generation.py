from datetime import datetime
from app.report.reports_generation import save_json_report_to_file
from sqlalchemy import text

from app import db

BASE_DIRECTORY_REPORTS = 'app/static/reports/'
GENERAL_REPORT_DIRECTORY = BASE_DIRECTORY_REPORTS + 'signal_reports'


def generate_json_signal_reports(init_date, last_date):
    """
    Calculate the network report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    report = signal_strength_mean_for_antenna(init_date, last_date)

    save_json_report_to_file(report, init_date.year, init_date.month, GENERAL_REPORT_DIRECTORY,
                             "network_report_")



# Signal strength mean by antenna
def signal_strength_mean_for_antenna(min_date=datetime(2015, 1, 1),
                                     max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""SELECT
      c2.antenna_id, c2.mnc, c2.mcc,
      c2.size AS observations,
      c2.ponderation / c2.size AS signal_mean
    FROM
    (SELECT
      sum(c1.size) as size,
      sum(c1.ponderation) as ponderation,
      c1.mnc, c1.mcc, c1.antenna_id
    FROM
    (SELECT
      telephony_observation_events.signal_strength_size as size,
      telephony_observation_events.signal_strength_size * telephony_observation_events.signal_strength_mean as ponderation,
      carriers.mnc as mnc,
      carriers.mcc as mcc,
      antennas.id as antenna_id
    FROM
      public.antennas,
      public.gsm_events,
      public.events,
      public.sims,
      public.telephony_observation_events,
      public.carriers
    WHERE
      gsm_events.antenna_id = antennas.id AND
      gsm_events.id = events.id AND
      events.sim_serial_number = sims.serial_number AND
      sims.carrier_id = carriers.id AND
      telephony_observation_events.id = gsm_events.id AND
      events.date BETWEEN :min_date AND :max_date
    ) AS c1
    GROUP BY mnc, mcc, antenna_id) AS c2;""")

    result = db.session.query().add_columns("antenna_id, mnc, mcc, observations, signal_mean").from_statement(
        stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()
