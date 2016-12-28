from app import db
from app.models.event import Event


class TrafficEvent(Event):
    '''
    Traffic events model class
    '''
    __tablename__ = 'traffic_events'

    id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    network_type = db.Column(db.Integer)
    rx_bytes = db.Column(db.BigInteger)
    tx_bytes = db.Column(db.BigInteger)
    rx_packets = db.Column(db.BigInteger)
    tx_packets = db.Column(db.BigInteger)
    tcp_rx_bytes = db.Column(db.BigInteger)
    tcp_tx_bytes = db.Column(db.BigInteger)


