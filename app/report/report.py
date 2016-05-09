from datetime import datetime


def generate_report():
    print("Generar reportes")


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


# Equipos por compania
def total_device_for_carrier(min_date=datetime(2015, 1, 1),
                             max_date=None):
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    result = db.session.query(Carrier).add_columns("devices_count").from_statement(text('''
    SELECT carriers.*, devices_count
     FROM
     (SELECT consulta_1.id, count(id) as devices_count
     FROM
     (SELECT DISTINCT devices.device_id, carriers.*
     FROM devices
     JOIN devices_sims ON devices.device_id = devices_sims.device_id
     JOIN sims ON sims.serial_number = devices_sims.sim_id
     JOIN carriers on sims.carrier_id = carriers.id
     WHERE devices.creation_date BETWEEN :min_date AND :max_date) as consulta_1
     GROUP BY consulta_1.id) as consulta_2
     JOIN carriers ON consulta_2.id = carriers.id''')).params(min_date=min_date, max_date=max_date)

    return result.all()


# Sims por compania
def total_sims_for_carrier(min_date=datetime(2015, 1, 1),
                           max_date=None):
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    result = db.session.query(Carrier).add_columns("sims_count").from_statement(text('''
    SELECT carriers.*, sims_count
    FROM carriers
    JOIN
    (SELECT carrier_id, count(*) AS sims_count
    FROM sims
    WHERE sims.creation_date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id) as consulta_1
    ON carriers.id=consulta_1.carrier_id''')).params(min_date=min_date, max_date=max_date)

    return result.all()


# Mediciones efectuadas por compania
def total_events_for_carrier(min_date=datetime(2015, 1, 1),
                             max_date=None):
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    result = db.session.query(Carrier).add_columns("events_count").from_statement(text('''
    SELECT carriers.*, events_count
    FROM carriers
    JOIN
    (SELECT carrier_id, count(*) AS events_count
    FROM events
    JOIN sims ON events.sim_serial_number = sims.serial_number
    WHERE events.date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id) as consulta_1
    ON carriers.id=consulta_1.carrier_id''')).params(min_date=min_date, max_date=max_date)

    return result.all()
