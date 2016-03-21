from app import db
from app.models.antenna_gsm_event import antennas_gsm_events
from app.models.telephony_observation_event import TelephonyObservationEvent


class GsmEvent(TelephonyObservationEvent):
    '''
    Clase para los eventos de observacion de telefonía tipo Gsm
    '''
    __tablename__ = 'gsm_events'
    __mapper_args__ = {'polymorphic_identity': 'gsm_event'}

    id = db.Column(db.Integer, db.ForeignKey('telephony_observation_events.id'), primary_key=True)
    gsm_cid = db.Column(db.Integer)
    gsm_lac = db.Column(db.Integer)
    gsm_psc = db.Column(db.Integer)
    signal_ber_size = db.Column(db.Integer)
    signal_ber_mean = db.Column(db.Float)
    signal_ber_variance = db.Column(db.Float)
    antennas = db.relationship('Antenna', secondary=antennas_gsm_events,
                               backref=db.backref('gsm_events', lazy='dynamic'), lazy='dynamic')

    def __init__(self, date, app_version_code, sim_serial_number, device_id, telephony_standard, network_type, gsm_cid,
                 gsm_lac, gsm_psc, signal_strength_size=None, signal_strength_mean=None, signal_strength_variance=None,
                 signal_ber_size=None, signal_ber_mean=None, signal_ber_variance=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.signal_strength_size = signal_strength_size
        self.signal_strength_mean = signal_strength_mean
        self.signal_strength_variance = signal_strength_variance
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.gsm_psc = gsm_psc
        self.signal_ber_size = signal_ber_size
        self.signal_ber_mean = signal_ber_mean
        self.signal_ber_variance = signal_ber_variance

    def __repr__(self):
        return '<GsmEvent, id: %r, date: %r>' % (self.id, self.date)
