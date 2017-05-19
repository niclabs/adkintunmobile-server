from app import db
from app.models.base_model import BaseModel


class ConnectivityEvent(BaseModel):
    '''
    Clase para los eventos de conectividad
    '''
    __tablename__ = 'connectivity_events'

    id = db.Column(db.Integer, primary_key=True)
    detailed_state = db.Column(db.Integer)
    available = db.Column(db.Boolean)
    connected = db.Column(db.Boolean)
    roaming = db.Column(db.Boolean)
    connection_type = db.Column(db.Integer)
    connection_type_other = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None, detailed_state=None,
                 available=None, connected=None, roaming=None, connection_type=None, connection_type_other=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.detailed_state = detailed_state
        self.available = available
        self.connected = connected
        self.roaming = roaming
        self.connection_type = connection_type
        self.connection_type_other = connection_type_other

    def __repr__(self):
        return '<ConnectivityEvent, id: %r, date: %r>' % (self.id, self.date)
