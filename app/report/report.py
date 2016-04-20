

def generate_report():
    print("Generar reporte")


# Total de equipos que han entregado datos
def totalDevicesReported():
    from app.models.device import Device
    return Device.query.filter(Device.events != None).count()

# Total de sims registradas
def totalSimsRegistered():
    from app.models.sim import Sim
    return Sim.query.count()

# Total de mediciones de señal registradas (GSM)
def totalGSMEvents():
    from app.models.gsm_event import GsmEvent
    return GsmEvent.query.count()

# Equipos por compania
def totalDeviceForCarrier():
    from app.models.sim import Sim
    from app.models.device import Device
    from sqlalchemy import func
    from app import db
    from app.models.device_sim import devices_sims
    return Device.query.join(devices_sims).join(Sim).group_by(Sim.carrier_id).all()
