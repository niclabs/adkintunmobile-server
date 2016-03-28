from app import db
from app.models.event import Event


class TrafficEvent(Event):
    '''
    Clase para los eventos de trafico
    '''
    __tablename__ = 'traffic_events'
    # __mapper_args__ = {'polymorphic_identity': 'Traffic_event'}

    id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    network_type = db.Column(db.Integer)
    rx_bytes = db.Column(db.BigInteger)
    tx_bytes = db.Column(db.BigInteger)
    rx_packets = db.Column(db.BigInteger)
    tx_packets = db.Column(db.BigInteger)
    tcp_rx_bytes = db.Column(db.BigInteger)
    tcp_tx_bytes = db.Column(db.BigInteger)

    # # Herencia
    # type_traffic_event = db.Column(db.String(50))
    # __mapper_args__ = {'polymorphic_on': type_traffic_event}
