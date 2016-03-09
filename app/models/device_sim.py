from sqlalchemy import Column, Integer, Date
from sqlalchemy.sql.schema import ForeignKey
from . import base_model


class DeviceSim(base_model.BaseModel):
    '''
    Clase device_sim, que crea una relación entre un device y una tarjeta sim.
    '''
    __tablename__ = 'devices_sims'
    id = Column(Integer, primary_key=True)
    creation_date = Column(Date())
    device = Column(Integer, ForeignKey("device.device_id"))
    sim = Column(Integer, ForeignKey("sim.serial_number"))

    def __init__(self, device, sim):
        self.device = device
        self.sim = sim

    def __repr__(self):
        return '<DeviceSim, id %r, device: %r, sim: %r>' % \
               (self.id, self.device.device_id, self.sim.serial_number)
