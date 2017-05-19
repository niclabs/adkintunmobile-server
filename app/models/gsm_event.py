from app import db
from app.models.base_model import BaseModel


class GsmEvent(BaseModel):
    '''
    Gsm observation events model class
    '''
    __tablename__ = 'gsm_events'

    id = db.Column(db.Integer, primary_key=True)
    gsm_psc = db.Column(db.Integer)
    signal_ber_size = db.Column(db.Integer)
    signal_ber_mean = db.Column(db.Float)
    signal_ber_variance = db.Column(db.Float)
    gsm_lac = db.Column(db.Integer)
    gsm_cid = db.Column(db.Integer)
    antenna_id = db.Column(db.Integer, db.ForeignKey('antennas.id'))
    telephony_standard = db.Column(db.Integer)
    network_type = db.Column(db.Integer)
    signal_strength_size = db.Column(db.Integer)
    signal_strength_mean = db.Column(db.Float)
    signal_strength_variance = db.Column(db.Float)
    mnc = db.Column(db.Integer)
    mcc = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None, antenna_id=None,
                 telephony_standard=None, network_type=None, gsm_psc=None, gsm_cid=None, gsm_lac=None,
                 signal_strength_size=None, signal_strength_mean=None, signal_strength_variance=None,
                 signal_ber_size=None, signal_ber_mean=None, signal_ber_variance=None, mnc=None, mcc=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.antenna_id = antenna_id
        self.signal_strength_size = signal_strength_size
        self.signal_strength_mean = signal_strength_mean
        self.signal_strength_variance = signal_strength_variance
        self.gsm_psc = gsm_psc
        self.signal_ber_size = signal_ber_size
        self.signal_ber_mean = signal_ber_mean
        self.signal_ber_variance = signal_ber_variance
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.mnc = mnc
        self.mcc = mcc

    def __repr__(self):
        return '<GsmEvent, id: %r, date: %r>' % (self.id, self.date)
