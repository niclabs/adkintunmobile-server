from sqlalchemy import Column, Integer, String
from . import base_model


class Carrier(base_model.BaseModel):
    '''
    Clase empresa de telecomunicaciones.
    name: Nombre de la empresa (Claro, Entel, etc.)
    '''
    __tablename__='carriers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    mcc = Column(Integer)
    mnc = Column(Integer)

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Telco %r>' % (self.name)
