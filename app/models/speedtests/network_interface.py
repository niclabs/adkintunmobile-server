from app import db
from app.models.base_model import BaseModel


class NetworkInterface(BaseModel):
    '''
    network interface model class
    '''
    __tablename__ = 'network_interfaces'

    id = db.Column(db.Integer, primary_key=True)
    active_interface = db.Column(db.Integer)
    ssid = db.Column(db.String(50))
    bssid = db.Column(db.String(50))
    gsm_cid = db.Column(db.Integer)
    gsm_lac = db.Column(db.Integer)
    network_type = db.Column(db.Integer)

    def __init__(self, active_interface=None, ssid=None, bssid=None, gsm_cid=None, gsm_lac=None, network_type=None):
        self.active_interface = active_interface
        self.ssid = ssid
        self.bssid = bssid
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.network_type = network_type

    def __repr__(self):
        return '<NetworkInterface, id: %r, Active interface: %r>' % (self.id, self.active_interface)
