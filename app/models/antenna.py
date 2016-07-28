from app import db
from app.models import base_model
from sqlalchemy import UniqueConstraint


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

    def __init__(self, cid=None, lac=None, lat=None, lon=None):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "<Antenna, id: %r,  cid: %r, lac: %r, carrier: %r,>" % (self.id, self.cid, self.lac, self.carrier_id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "cid": self.cid,
            "lac": self.lac,
            "lat": self.lat,
            "lon": self.lon,
            "carrier_id": self.carrier_id
        }
