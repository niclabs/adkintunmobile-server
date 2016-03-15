from app import db
from app.models.event import Event


class ConnectivityEvent(Event):
    '''
    Clase para los eventos de conectividad
    '''
    __tablename__ = 'connectivity_events'

    detailed_state = db.Column(db.Integer)
    available = db.Column(db.Boolean)
    connected = db.Column(db.Boolean)
    roaming = db.Column(db.Boolean)
    connection_type = db.Column(db.Integer)
    connection_type_other = db.Column(db.Integer)

    def __init__(self, date, app_version_code, detailed_state, available, connected, roaming, connection_type,
                 connection_type_other):
        self.date = date
        self.app_version_code = app_version_code
        self.detailed_state = detailed_state
        self.available = available
        self.connected = connected
        self.roaming = roaming
        self.connection_type = connection_type
        self.connection_type_other = connection_type_other

    def __repr__(self):
        return '<ConnectivityEvent, id: %r, date: %r>' % (self.id, self.date)