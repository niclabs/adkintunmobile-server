from app import db
from app.models.event import Event
from sqlalchemy.ext.declarative import declared_attr


class TelephonyObservationEvent(Event):
    '''
    Clase para los eventos de observaciones de telefonía
    '''
    __tablename__ = 'telephony_observation_events'
    __mapper_args__ = {'polymorphic_identity': 'telephony_observation_event'}

    id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)

    telephony_standard = db.Column(db.Integer)
    network_type = db.Column(db.Integer)
    signal_strength_size = db.Column(db.Integer)
    signal_strength_mean = db.Column(db.Float)
    signal_strength_variance = db.Column(db.Float)

    @declared_attr
    def carrier_id(cls):
        return db.Column(db.Integer, db.ForeignKey("carriers.id"))

    # Herencia
    type_telephony_observation = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_on': type_telephony_observation}
