from app import db
from app.models.base_model import BaseModel


class Event(BaseModel):
    '''
    Events model class
    '''
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))

