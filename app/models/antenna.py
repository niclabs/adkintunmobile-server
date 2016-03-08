from sqlalchemy import Column, Integer, Float
from sqlalchemy.sql.schema import ForeignKey
from . import base_model


class Antenna(base_model.BaseModel):
    '''
    Clase antena.
    '''
    __tablename__ = 'antennas'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer)
    lac = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)
    carrier = Column(Integer, ForeignKey("carriers.id"))

    def __init__(self, cid, lac, lat, long, carrier):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.long = long
        self.carrier = carrier

    def __repr__(self):
        return '<Antenna, id: %r, carrier: %r, cid: %r, lac: %r>' % (self.id, self.carrier, self.cid, self.lac)
