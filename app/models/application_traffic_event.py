from app import db
from app.models.traffic_event import TrafficEvent


class ApplicationTrafficEvent(TrafficEvent):
    '''
    Clase para los eventos de Trafico de application
    '''
    __tablename__ = 'application_traffic_events'
    __mapper_args__ = {'polymorphic_identity': 'application_traffic_event'}

    id = db.Column(db.Integer, db.ForeignKey('traffic_events.id'), primary_key=True)

    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))

    def __init__(self, date, app_version_code, sim_serial_number, device_id, network_type, rx_bytes, tx_bytes,
                 rx_packets, tx_packets, tcp_rx_bytes, tcp_tx_bytes, application_id):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.network_type = network_type
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.tcp_rx_bytes = tcp_rx_bytes
        self.tcp_tx_bytes = tcp_tx_bytes
        self.application_id = application_id

    def __repr__(self):
        return '<ApplicationTrafficEvent, id: %r, date: %r, application: %r>' % (self.id, self.date, self.application)
