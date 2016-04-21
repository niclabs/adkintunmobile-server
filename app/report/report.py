def generate_report():
    print("Generar reporte")


# Total de equipos que han entregado datos
def total_devices_reported():
    from app.models.device import Device
    return Device.query.filter(Device.events != None).count()


# Total de sims registradas
def total_sims_registered():
    from app.models.sim import Sim
    return Sim.query.count()


# Total de mediciones de señal registradas (GSM)
def total_gsm_events():
    from app.models.gsm_event import GsmEvent
    return GsmEvent.query.count()


# Equipos por compania
def total_device_for_carrier():
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    result = db.session.query(Carrier).add_columns("devices_count").from_statement(text('''
    SELECT carriers.*, devices_count
     FROM
     (SELECT consulta_1.id, count(id) as devices_count
     FROM
     (SELECT DISTINCT devices.device_id, carriers.*
     FROM devices
     JOIN devices_sims ON devices.device_id = devices_sims.device_id
     JOIN sims ON sims.serial_number = devices_sims.sim_id
     JOIN carriers on sims.carrier_id = carriers.id) as consulta_1
     GROUP BY consulta_1.id) as consulta_2
     JOIN carriers ON consulta_2.id = carriers.id'''))

    return result.all()


# Sims por compania
def total_sims_for_carrier():
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    result = db.session.query(Carrier).add_columns("sims_count").from_statement(text('''
    SELECT carriers.*, sims_count
    FROM carriers
    JOIN
    (SELECT carrier_id, count(*) AS sims_count
    FROM sims
    GROUP BY carrier_id) as consulta_1
    ON carriers.id=consulta_1.carrier_id'''))

    return result.all()


# Mediciones efectuadas por compania
def total_events_for_carrier():
    from app.models.carrier import Carrier
    from app import db
    from sqlalchemy import text

    result = db.session.query(Carrier).add_columns("events_count").from_statement(text('''
    SELECT carriers.*, events_count
    FROM carriers
    JOIN
    (SELECT carrier_id, count(*) AS events_count
    FROM events
    JOIN sims ON events.sim_serial_number = sims.serial_number
    GROUP BY carrier_id) as consulta_1
    ON carriers.id=consulta_1.carrier_id'''))

    return result.all()

