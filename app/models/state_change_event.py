from app import db
from app.models.base_model import BaseModel


class StateChangeEvent(BaseModel):
    '''
    Clase para los eventos de cambio de estado
    '''
    __tablename__ = 'state_change_events'

    id = db.Column(db.Integer, primary_key=True)
    state_type = db.Column(db.Integer)
    state = db.Column(db.Integer)
    event_type = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"), index=True)

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None, state_type=None,
                 state=None, event_type=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.state_type = state_type
        self.state = state
        self.event_type = event_type

    def __repr__(self):
        return '<StateChangeEvent, id: %r, date: %r>' % (self.id, self.date)
