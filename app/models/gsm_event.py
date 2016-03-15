from app import db
from app.models.telephony_observation_event import TelephonyObservationEvent


class GsmEvent(TelephonyObservationEvent):
    '''
    Clase para los eventos de observacion de telefonía tipo Gsm
    '''
    __tablename__ = 'gsm_events'

    gsm_cid = db.Column(db.Integer)
    gsm_lac = db.Column(db.Integer)
    gsm_psc = db.Column(db.Integer)

    def __init__(self, date, app_version_code, telephony_standard, network_type, gsm_cid, gsm_lac, gsm_psc):
        self.date = date
        self.app_version_code = app_version_code
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.gsm_psc = gsm_psc

    def __repr__(self):
        return '<GsmEvent, id: %r, date: %r>' % (self.id, self.date)
