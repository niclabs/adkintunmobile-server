from app import db
from app.models import base_model


class Carrier(base_model.BaseModel):
    '''
    Carrier model class
    '''
    __tablename__ = 'carriers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    mcc = db.Column(db.Integer)
    mnc = db.Column(db.Integer)
    sims = db.relationship('Sim', backref='carrier', lazy='dynamic')
    telephony_observation_events = db.relationship('TelephonyObservationEvent', backref='carrier', lazy='dynamic')
    antennas = db.relationship("Antenna", backref='carrier', lazy='dynamic')

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Carrier %r>' % (self.name)

    def add_sim(self, sim):
        """
        Add sim to sims parameter in a carrier, just if it was not previously added.
        """
        from app.models.sim import Sim
        existent_sim = self.sims.filter(Sim.serial_number == sim.serial_number).first()
        if not existent_sim:
            self.sims.append(sim)

    @staticmethod
    def get_carrier_or_add_it(args):
        """
        Search a carrier and retrieve it if exist, else create a new one and retrieve it.
        """
        carrier = Carrier.query.filter(Carrier.mnc == args["mnc"], Carrier.mcc == args["mcc"]).first()
        if not carrier:
            carrier = Carrier(mnc=args["mnc"], mcc=args["mcc"], name="Unknown")
            db.session.add(carrier)
            db.session.commit()
        return carrier
