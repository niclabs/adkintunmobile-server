from app import db
from app.models.event import Event


class TelephonyObservationEvent(Event):
    '''
    Clase para los eventos de observacioens de telefonía
    '''
    __tablename__ = 'telephony_observation_events'
    __abstract__ = True

    telephony_standard = db.Column(db.Integer)
    network_type = db.Column(db.Integer)

    #TODO vincular con carrier