from app import db
from app.models.base_model import BaseModel
from sqlalchemy.ext.declarative import declared_attr


class TelephonyObservationEvent(BaseModel):
    '''
    Telephony observation model class
    '''
    __tablename__ = 'telephony_observation_events'

    id = db.Column(db.Integer, primary_key=True)

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

