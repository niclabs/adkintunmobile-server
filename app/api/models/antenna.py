from sqlalchemy import Column, Integer, String, Float
from . import base_model


class Antenna(base_model.BaseModel):
    '''
    Clase antena.
    '''
    __tablename__='antennas'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer)
    lac = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)

    def __init__(self, cid, lac):
        self.cid = cid
        self.lac = lac

    def __repr__(self):
        return '<Antenna, cid: %r, lac: %r>' % (self.cid, self.lac)
