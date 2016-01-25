from sqlalchemy import Column, Integer, Date
from app import db
from . import model_mixin


class Sim(db.Model, model_mixin.ModelMixin):
    '''
    Clase tarjeta sim.
    '''
    __tablename__='sims'
    serial_number = Column(Integer, primary_key=True)
    creation_date = Column(Date())

    def __init__(self, creation_date):
        self.creation_date = creation_date

    def __repr__(self):
        return '<Sim, serial_number: %r, creation_date: %r>' % \
        (self.serial_number, self.creation_date)
