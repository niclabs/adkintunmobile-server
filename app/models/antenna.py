from app import db
from app.models.antenna_carrier import antennas_carriers
from app.models import base_model


class Antenna(base_model.BaseModel):
    '''
    Clase antena.
    '''
    __tablename__ = 'antennas'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    carriers = db.relationship('Carrier', secondary=antennas_carriers,
                               backref=db.backref('antennas', lazy='dynamic'), lazy='dynamic')  # relationship

    def __init__(self, cid=None, lac=None, lat=None, lon=None):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Antenna, id: %r,  cid: %r, lac: %r, carriers: %r,>' % (self.id, self.cid, self.lac, self.carriers)
