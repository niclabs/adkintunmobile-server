from datetime import datetime

from app import db
from app.models.base_model import BaseModel


class WifiTrafficEvent(BaseModel):
    '''
    Clase para los eventos de Trafico de wifi
    '''
    __tablename__ = 'wifi_traffic_events'

    id = db.Column(db.Integer, primary_key=True)
    network_type = db.Column(db.Integer)
    rx_bytes = db.Column(db.BigInteger)
    tx_bytes = db.Column(db.BigInteger)
    rx_packets = db.Column(db.BigInteger)
    tx_packets = db.Column(db.BigInteger)
    tcp_rx_bytes = db.Column(db.BigInteger)
    tcp_tx_bytes = db.Column(db.BigInteger)
    date = db.Column(db.DateTime, index=True)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))

    def __init__(self, date: datetime = None, app_version_code=None, sim_serial_number=None, device_id=None,
                 network_type=None,
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
        return '<WifiTrafficEvent, id: %r, date: %r>' % (self.id, self.date)
