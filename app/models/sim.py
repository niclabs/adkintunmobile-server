from app import db
from app.models import base_model
from app.models.device_sim import devices_sims


class Sim(base_model.BaseModel):
    '''
    Clase tarjeta sim.
    '''
    __tablename__ = 'sims'

    serial_number = db.Column(db.BigInteger, primary_key=True)
    creation_date = db.Column(db.Date())
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))
    devices = db.relationship('Device', secondary=devices_sims, backref=db.backref('sims', lazy='dynamic'),
                              lazy='dynamic')
    events = db.relationship('Event', backref='sim', lazy='dynamic')

    def __init__(self, serial_number=None, creation_date=None, carrier_id=None):
        self.serial_number = serial_number
        self.creation_date = creation_date
        self.carrier_id = carrier_id

    def __repr__(self):
        return '<Sim, serial_number: %r, creation_date: %r, carrier: %r, carrier_id: %r>' % \
               (self.serial_number, self.creation_date, self.carrier, self.carrier_id)
