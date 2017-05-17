from app import db
from app.models.base_model import BaseModel


class TrafficEvent(BaseModel):
    '''
    Traffic events model class
    '''
    __tablename__ = 'traffic_events'

    id = db.Column(db.Integer, primary_key=True)
    network_type = db.Column(db.Integer)
    rx_bytes = db.Column(db.BigInteger)
    tx_bytes = db.Column(db.BigInteger)
    rx_packets = db.Column(db.BigInteger)
    tx_packets = db.Column(db.BigInteger)
    tcp_rx_bytes = db.Column(db.BigInteger)
    tcp_tx_bytes = db.Column(db.BigInteger)
    date = db.Column(db.DateTime)
    app_version_code = db.Column(db.String(10))
    sim_serial_number = db.Column(db.String(50), db.ForeignKey("sims.serial_number"))
    device_id = db.Column(db.String(50), db.ForeignKey("devices.device_id"))

