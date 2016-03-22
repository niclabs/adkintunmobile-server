from app import db
from app.models.traffic_event import TrafficEvent


class MobileTrafficEvent(TrafficEvent):
    '''
    Clase para los eventos de Trafico de mobile
    '''
    __tablename__ = 'mobile_traffic_events'
    __mapper_args__ = {'polymorphic_identity': 'mobile_traffic_event'}

    id = db.Column(db.Integer, db.ForeignKey('traffic_events.id'), primary_key=True)

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None, network_type=None,
                 rx_bytes=None, tx_bytes=None, rx_packets=None, tx_packets=None, tcp_rx_bytes=None, tcp_tx_bytes=None):
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

    def __repr__(self):
        return '<MobileChangeEvent, id: %r, date: %r>' % (self.id, self.date)
