from app import db
from app.models import base_model


class Device(base_model.BaseModel):
    '''
    Clase Dispositivo.
    '''
    __tablename__ = 'devices'
    device_id = db.Column(db.BigInteger, primary_key=True)
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
    events = db.relationship('Event', backref='device', lazy='dynamic')

    def __init__(self, brand=None, board=None, build_id=None, device=None, hardware=None,
                 manufacturer=None, model=None, release=None, release_type=None, product=None, sdk=None,
                 creation_date=None):
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
        self.creation_date = creation_date

    def __repr__(self):
        return '<Device %r, device_id %r>' % (self.device, self.device_id)

    @staticmethod
    def store_if_no_exist(args):
        from datetime import datetime

        device = Device.query.filter(Device.build_id == args['build_id']).first()
        if not device:
            device = Device(
                    brand=args['brand'],
                    board=args['board'],
                    build_id=args['build_id'],
                    device=args['device'],
                    hardware=args['hardware'],
                    manufacturer=args['manufacturer'],
                    model=args['model'],
                    release=args['release'],
                    release_type=args['release_type'],
                    product=args['product'],
                    sdk=args['sdk'],
                    creation_date=datetime.now().date())
            db.session.add(device)
        return device