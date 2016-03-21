from app import db
from app.models.event import Event


class StateChangeEvent(Event):
    '''
    Clase para los eventos de cambio de estado
    '''
    __tablename__ = 'state_change_events'
    __mapper_args__ = {'polymorphic_identity': 'state_change_event'}

    id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    state_type = db.Column(db.Integer)
    state = db.Column(db.Integer)
    event_type = db.Column(db.Integer)

    def __init__(self, date, app_version_code, sim_serial_number, device_id, state_type, state, event_type):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.state_type = state_type
        self.state = state
        self.event_type = event_type

    def __repr__(self):
        return '<StateChangeEvent, id: %r, date: %r>' % (self.id, self.date)
