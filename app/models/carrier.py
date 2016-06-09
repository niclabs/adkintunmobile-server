from app import db
from app.models import base_model


class Carrier(base_model.BaseModel):
    '''
    Clase empresa de telecomunicaciones.
    name: Nombre de la empresa (Claro, Entel, etc.)
    '''
    __tablename__ = 'carriers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    mcc = db.Column(db.Integer)
    mnc = db.Column(db.Integer)
    sims = db.relationship('Sim', backref='carrier', lazy='dynamic')
    telephony_observation_events = db.relationship('TelephonyObservationEvent', backref='carrier', lazy='dynamic')

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Carrier %r>' % (self.name)


    carriers = {
        '': 'none',
        'entel': 'entel',
        'movistar': 'movistar',
        'claro': 'claro',
        'WOM': 'wom',
        'Telefónica del Sur': 'tds',
        'VTR Móvil': 'vtrm',
        'Virgin Mobile': 'virginm',
        'Will': 'will',
        'Nextel': 'nextel',
        'Celupago': 'celupago',
        'Colo-Colo Móvil Wanderers Móvil': 'ccwm',
        'Netline': 'netline'}


    def add_sim(self, sim):
        from app.models.sim import Sim
        existent_sim = self.sims.filter(Sim.serial_number == sim.serial_number).first()
        if not existent_sim:
            self.sims.append(sim)
