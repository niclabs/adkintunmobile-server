from app import db
from app.models.base_model import BaseModel


class CdmaEvent(BaseModel):
    '''
    Clase para los eventos de observacion de telefonía tipo Cdma
    '''
    __tablename__ = 'cdma_events'

    id = db.Column(db.Integer, primary_key=True)
    cdma_base_latitude = db.Column(db.Integer)
    cdma_base_longitude = db.Column(db.Integer)
    cdma_base_station_id = db.Column(db.Integer)
    network_id = db.Column(db.Integer)
    system_id = db.Column(db.Integer)
    cdma_ecio_size = db.Column(db.Integer)
    cdma_ecio_mean = db.Column(db.Float)
    cdma_ecio_variance = db.Column(db.Float)
    evdo_dbm_size = db.Column(db.Integer)
    evdo_dbm_mean = db.Column(db.Float)
    evdo_dbm_variance = db.Column(db.Float)
    evdo_ecio_size = db.Column(db.Integer)
    evdo_ecio_mean = db.Column(db.Float)
    evdo_ecio_variance = db.Column(db.Float)
    evdo_snr_size = db.Column(db.Integer)
    evdo_snr_mean = db.Column(db.Float)
    evdo_snr_variance = db.Column(db.Float)
    telephony_standard = db.Column(db.Integer)
    network_type = db.Column(db.Integer)
    signal_strength_size = db.Column(db.Integer)
    signal_strength_mean = db.Column(db.Float)
    signal_strength_variance = db.Column(db.Float)
    mnc = db.Column(db.Integer)
    mcc = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None,
                 telephony_standard=None, network_type=None, cdma_base_latitude=None, cdma_base_longitude=None,
                 cdma_base_station_id=None, network_id=None, system_id=None,
                 signal_strength_size=None, signal_strength_mean=None, signal_strength_variance=None,
                 cdma_ecio_size=None, cdma_ecio_mean=None, cdma_ecio_variance=None, evdo_dbm_size=None,
                 evdo_dbm_mean=None, evdo_dbm_variance=None, evdo_ecio_size=None, evdo_ecio_mean=None,
                 evdo_ecio_variance=None, evdo_snr_size=None, evdo_snr_mean=None, evdo_snr_variance=None, mnc=None,
                 mcc=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.signal_strength_size = signal_strength_size
        self.signal_strength_mean = signal_strength_mean
        self.signal_strength_variance = signal_strength_variance
        self.cdma_base_latitude = cdma_base_latitude
        self.cdma_base_longitud = cdma_base_longitude
        self.cdma_base_station_id = cdma_base_station_id
        self.network_id = network_id
        self.system_id = system_id
        self.cdma_ecio_size = cdma_ecio_size
        self.cdma_ecio_mean = cdma_ecio_mean
        self.cdma_ecio_variance = cdma_ecio_variance
        self.evdo_dbm_size = evdo_dbm_size
        self.evdo_dbm_mean = evdo_dbm_mean
        self.evdo_dbm_variance = evdo_dbm_variance
        self.evdo_ecio_size = evdo_ecio_size
        self.evdo_ecio_mean = evdo_ecio_mean
        self.evdo_ecio_variance = evdo_ecio_variance
        self.evdo_snr_size = evdo_snr_size
        self.evdo_snr_mean = evdo_snr_mean
        self.evdo_snr_variance = evdo_snr_variance
        self.mnc = mnc
        self.mcc = mcc

    def __repr__(self):
        return '<CdmaEvent, id: %r, date: %r>' % (self.id, self.date)
