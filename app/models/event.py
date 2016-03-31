from app import db
from app.models.base_model import BaseModel


class Event(BaseModel):
    '''
    Clase Eventos, base de todos los eventos
    '''
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.BigInteger, db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.BigInteger, db.ForeignKey("devices.device_id"))

    # Herencia
    type = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_on': type}
