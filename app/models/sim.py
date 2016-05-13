from app import db
from app.models import base_model
from app.models.device_sim import devices_sims


class Sim(base_model.BaseModel):
    '''
    Clase tarjeta sim.
    '''
    __tablename__ = 'sims'

    serial_number = db.Column(db.String(50), primary_key=True)
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

    @staticmethod
    def store_if_not_exist(args):
        from datetime import datetime

        sim = Sim.query.filter(Sim.serial_number == args['serial_number']).first()

        if not sim:
            sim = Sim(serial_number=args['serial_number'], creation_date=datetime.now())
            db.session.add(sim)
        return sim

    def add_device(self, device):
        from app.models.device import Device

        existent_device = self.devices.filter(Device.device_id == device.device_id).first()
        if not existent_device:
            self.devices.append(device)