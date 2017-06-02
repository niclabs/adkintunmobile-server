from datetime import datetime

from sqlalchemy import text

from app import db
from app.models.antenna import Antenna
from app.models.sim import Sim
from app.models.telephony_observation_event import TelephonyObservationEvent
from app.report.reports_generation import save_json_report_to_file


def generate_json_4g_reports(init_date, last_date):
    """
    Calculate the network report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    report = network_report_for_4g(init_date, last_date)

    save_json_report_to_file(report, init_date.year, init_date.month,
                             "4g_report_")


# network report
def network_report_for_4g(min_date=datetime(2015, 1, 1),
                               max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""

    SELECT
        CASE WHEN gsm_events_4g_capable.network_type = 14 THEN '4G'
        ELSE 'OTHER' END as network_type,
        antennas_4g_capable.id as antenna,
        carriers.name as carrier,
        count(gsm_events_4g_capable.id) as size
    FROM
        (SELECT DISTINCT antennas.id
            FROM antennas, gsm_events
            WHERE
                gsm_events.date BETWEEN :min_date AND :max_date AND
                gsm_events.antenna_id = antennas.id AND
                gsm_events.network_type = 14) as antennas_4g_capable,
        (SELECT gsm_events.id, gsm_events.carrier_id, gsm_events.antenna_id, gsm_events.network_type
            FROM
             gsm_events,
             (SELECT DISTINCT gsm_events.device_id
                FROM gsm_events, devices
                WHERE
                    gsm_events.date BETWEEN :min_date AND :max_date AND
                    gsm_events.device_id = devices.device_id) as devices_4g_capable
            WHERE
                gsm_events.date BETWEEN :min_date AND :max_date AND
                gsm_events.device_id = devices_4g_capable.device_id
        ) as gsm_events_4g_capable,
        public.carriers
    WHERE
        gsm_events_4g_capable.date BETWEEN :min_date AND :max_date AND
        gsm_events_4g_capable.antenna_id = antennas_4g_capable.id AND
        gsm_events_4g_capable.carrier_id = carriers.id
    GROUP BY
        gsm_events_4g_capable.network_type,
        antennas_4g_capable.id,
        carriers.name
    ORDER BY
        carriers.name,
        antennas_4g_capable.id""")

    result = db.session.query(TelephonyObservationEvent.network_type, Antenna.id,
                              Sim.carrier_id).add_columns("size").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    final = [dict(network_type=row[0], antenna_id=row[1], carrier_id=row[2], size=row[3]) for row in
             result.all()]

    return final
