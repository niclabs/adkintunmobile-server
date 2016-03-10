from app import db
from . import base_model


class Device(base_model.BaseModel):
    '''
    Clase Dispositivo.
    '''
    __tablename__ = 'devices'
    device_id = db.Column (db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    board = db.Column(db.String(50))
    build_id = db.Column(db.String(50))
    creation_date = db.Column(db.Date())
    device = db.Column(db.String(50))
    hardware = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    release = db.Column(db.String(50))
    release_type = db.Column(db.String(50))
    product = db.Column(db.String(50))
    sdk = db.Column(db.Integer)

    def __init__(self, brand, board, build, build_id, device, hardware,
                 manufacturer, model, release, release_type, product, sdk):
        self.brand = brand
        self.board = board
        self.build_id = build_id
        self.device = device
        self.hardware = hardware
        self.manufacturer = manufacturer
        self.model = model
        self.release = release
        self.release_type = release_type
        self.product = product
        self.sdk = sdk

    def __repr__(self):
        return '<Device %r, device_id %r>' % (self.device, self.device_id)
