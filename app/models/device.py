from sqlalchemy import Column, Integer, String, Date
from . import base_model


class Device(base_model.BaseModel):
    '''
    Clase Dispositivo.
    '''
    __tablename__ = 'devices'
    device_id = Column(Integer, primary_key=True)
    brand = Column(String(50))
    board = Column(String(50))
    build_id = Column(String(50))
    creation_date = Column(Date())
    device = Column(String(50))
    hardware = Column(String(50))
    manufacturer = Column(String(50))
    model = Column(String(50))
    release = Column(String(50))
    release_type = Column(String(50))
    product = Column(String(50))
    sdk = Column(Integer)

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
