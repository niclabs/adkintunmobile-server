from app import db
from app.models.event import Event
from sqlalchemy.ext.declarative import declared_attr


class TelephonyObservationEvent(Event):
    '''
    Telephony observation model class
    '''
    __tablename__ = 'telephony_observation_events'

    id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)

    telephony_standard = db.Column(db.Integer)
    network_type = db.Column(db.Integer)
    signal_strength_size = db.Column(db.Integer)
    signal_strength_mean = db.Column(db.Float)
    signal_strength_variance = db.Column(db.Float)
    mnc = db.Column(db.Integer)
    mcc = db.Column(db.Integer)

    @declared_attr
    def carrier_id(cls):
        return db.Column(db.Integer, db.ForeignKey("carriers.id"))

