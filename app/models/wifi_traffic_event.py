from app.models.traffic_event import TrafficEvent


class WifiTrafficEvent(TrafficEvent):
    '''
    Clase para los eventos de Trafico de wifi
    '''
    __tablename__ = 'wifi_traffic_events'

    def __init__(self, date, app_version_code, network_type, rx_bytes, tx_bytes, rx_packets, tx_packets, tcp_rx_bytes,
                 tcp_tx_bytes):
        self.date = date
        self.app_version_code = app_version_code
        self.network_type = network_type
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.tcp_rx_bytes = tcp_rx_bytes
        self.tcp_tx_bytes = tcp_tx_bytes

    def __repr__(self):
        return '<WifiChangeEvent, id: %r, date: %r>' % (self.id, self.date)
