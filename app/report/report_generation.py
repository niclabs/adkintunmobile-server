from datetime import datetime


def generate_report():
    '''
    Función que calcula los valores del reporte y los guarda en las tablas correspondientes.
    Además, setea las fechas entre las cuales se hizo el reporte (muy importante) las cuales son als asignadas en la tabla de reportes
    :return: Nada
    '''

    # Seteamos fecha de cuando comienza el reporte
    actual_date = datetime.now()

    # Obtenemos fecha del último reporte
    from app.models.daily_report import DailyReport
    from app.models.total_report import TotalReport

    last_element = TotalReport.query.order_by(TotalReport.id.desc()).first()
    init_date = datetime(2015, 1, 2)

    if last_element:
        init_date = last_element.final_date

    # calcular todos los valores pertinentes
    total_devices = total_devices_reported(init_date, actual_date)
    total_sims = total_sims_registered(init_date, actual_date)
    total_gsm = total_gsm_events(init_date, actual_date)
    total_device_carrier = total_device_for_carrier(init_date, actual_date)
    total_sims_carrier = total_sims_for_carrier(init_date, actual_date)
    total_gsm_carrier = total_gsm_events_for_carrier(init_date, actual_date)

    from app.models.carrier import Carrier

    daily_report = DailyReport(init_date=init_date, final_date=actual_date, total_devices=total_devices,
                               total_sims=total_sims, total_events=total_gsm)
    total_report = TotalReport(init_date=init_date, final_date=actual_date)


    if last_element:
        for k in dir(last_element):
            if not k == 'init_date' and not k == 'actual_date' and not k=='id':
                setattr(total_report, k, getattr(last_element, k))

    total_report.total_events = total_report.total_events+total_gsm
    total_report.total_devices = total_report.total_devices+total_devices
    total_report.total_sims = total_report.total_sims+total_sims

    for element in total_device_carrier:
        carrier = Carrier.carriers.get(element.Carrier.name, 'none')
        setattr(daily_report, 'devices_' + carrier, element.devices_count)
        setattr(total_report, 'devices_' + carrier,
                    element.devices_count + getattr(total_report, 'devices_' + carrier))

    for element in total_sims_carrier:
        carrier = Carrier.carriers.get(element.Carrier.name, 'none')
        setattr(daily_report, 'sims_' + carrier, element.sims_count)
        setattr(total_report, 'sims_' + carrier, element.sims_count + getattr(total_report, 'sims_' + carrier))

    for element in total_gsm_carrier:
        carrier = Carrier.carriers.get(element.Carrier.name, 'none')
        setattr(daily_report, 'events_' + carrier, element.events_count)
        setattr(total_report, 'events_' + carrier,
                    element.events_count + getattr(total_report, 'events_' + carrier))

    from app import db
    db.session.add(daily_report)
    db.session.add(total_report)
    db.session.commit()

    print("Almacenados reportes de fecha " + str(actual_date))


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
def total_gsm_events_for_carrier(min_date=datetime(2015, 1, 1),
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
    FROM gsm_events
    JOIN events ON gsm_events.id = events.id
    JOIN sims ON events.sim_serial_number = sims.serial_number
    WHERE events.date BETWEEN :min_date AND :max_date
    GROUP BY carrier_id) as consulta_1
    ON carriers.id=consulta_1.carrier_id''')).params(min_date=min_date, max_date=max_date)

    return result.all()
