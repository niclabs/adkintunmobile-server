from sqlalchemy import UniqueConstraint

from app import db
from app.models import base_model


class Antenna(base_model.BaseModel):
    """
    Antenna Class.
    """
    __tablename__ = "antennas"
    __table_args__ = (UniqueConstraint("cid", "lac", "carrier_id", name="antenna_pk"), {})
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))
    gsm_events = db.relationship("GsmEvent", backref="antenna",
                                 lazy="dynamic")

    def __init__(self, cid=None, lac=None, lat=None, lon=None, carrier_id=None):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon
        self.carrier_id = carrier_id

    def __repr__(self):
        return "<Antenna, id: %r,  cid: %r, lac: %r, carrier: %r,>" % (self.id, self.cid, self.lac, self.carrier_id)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "cid": self.cid,
            "lac": self.lac,
            "lat": self.lat,
            "lon": self.lon,
            "carrier_id": self.carrier_id
        }

    @staticmethod
    def get_antenna_or_add_it(args):
        """
        Search an antenna and retrieve it if exist, else create a new one and retrieve it.
        """
        from app.models.carrier import Carrier
        carrier = Carrier.query.filter(mnc=args.mnc, mcc=args.mcc)
        antenna = Antenna.query.filter(lac=args.lac, cid=args.cid, carrier_id=carrier.id).first()
        if not antenna:
            from app import Session
            antenna = Antenna(lac=args.gsm_lac, cid=args.gsm_cid, carrier_id=carrier.id)
            session = Session()
            session.add(antenna)
            session.commit()
        return antenna
