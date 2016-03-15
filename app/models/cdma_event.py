from app import db
from app.models.telephony_observation_event import TelephonyObservationEvent


class CdmaEvent(TelephonyObservationEvent):
    '''
    Clase para los eventos de observacion de telefonía tipo Cdma
    '''
    __tablename__ = 'cdma_events'

    cdma_base_latitude = db.Column(db.Integer)
    cdma_base_longitude = db.Column(db.Integer)
    cdma_base_station_id = db.Column(db.Integer)
    network_id = db.Column(db.Integer)
    system_id = db.Column(db.Integer)

    # TODO agregar estos samples
    # Sample cdmaEcio
    # Sample evdoDbm
    # Sample evdoEcio
    # Sample evdoSnr

    def __init__(self, date, app_version_code, telephony_standard, network_type, cdma_base_latitude,
                 cdma_base_longitude, cdma_base_station_id, network_id, system_id):
        self.date = date
        self.app_version_code = app_version_code
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.cdma_base_latitude = cdma_base_latitude
        self.cdma_base_longitud = cdma_base_longitude
        self.cdma_base_station_id = cdma_base_station_id
        self.network_id = network_id
        self.system_id = system_id

    def __repr__(self):
        return '<CdmaEvent, id: %r, date: %r>' % (self.id, self.date)
