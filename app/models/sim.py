from sqlalchemy import Column, Integer, Date
from sqlalchemy.sql.schema import ForeignKey
from . import base_model


class Sim(base_model.BaseModel):
    '''
    Clase tarjeta sim.
    '''
    __tablename__ = 'sims'
    serial_number = Column(Integer, primary_key=True)
    creation_date = Column(Date())
    carrier = Column(Integer, ForeignKey("carriers.id"))

    def __init__(self, serial_number, creation_date, carrier):
        self.serial_number = serial_number
        self.creation_date = creation_date
        self.carrier = carrier

    def __repr__(self):
        return '<Sim, serial_number: %r, creation_date: %r, carrier: %r>' % \
               (self.serial_number, self.creation_date, self.carrier)
