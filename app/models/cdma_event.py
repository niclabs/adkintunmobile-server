from app import db
from app.models.telephony_observation_event import TelephonyObservationEvent


class CdmaEvent(TelephonyObservationEvent):
    '''
    Clase para los eventos de observacion de telefonía tipo Cdma
    '''
    __tablename__ = 'cdma_events'
    __mapper_args__ = {'polymorphic_identity': 'cdma_event'}

    id = db.Column(db.Integer, db.ForeignKey('telephony_observation_events.id'), primary_key=True)
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

    def __init__(self, date, app_version_code, sim_serial_number, device_id, telephony_standard, network_type,
                 cdma_base_latitude, cdma_base_longitude, cdma_base_station_id, network_id, system_id,
                 signal_strength_size=None, signal_strength_mean=None, signal_strength_variance=None,
                 cdma_ecio_size=None, cdma_ecio_mean=None, cdma_ecio_variance=None, evdo_dbm_size=None,
                 evdo_dbm_mean=None, evdo_dbm_variance=None, evdo_ecio_size=None, evdo_ecio_mean=None,
                 evdo_ecio_variance=None, evdo_snr_size=None, evdo_snr_mean=None, evdo_snr_variance=None):
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

    def __repr__(self):
        return '<CdmaEvent, id: %r, date: %r>' % (self.id, self.date)
