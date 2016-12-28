from app import db
from app.models.base_model import BaseModel


class VideoResult(BaseModel):
    '''
    network interface model class
    '''
    __tablename__ = 'video_results'

    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String(50))
    buffering_time = db.Column(db.BigInteger)
    loaded_fraction = db.Column(db.Float)
    downloaded_bytes = db.Column(db.BigInteger)

    # relationships
    media_test_report_id = db.Column(db.Integer, db.ForeingKey("media_test_report.id"))

    def __init__(self, quality=None, buffering_time=None, loaded_fraction=None, downloaded_bytes=None):
        self.quality = quality
        self.buffering_time = buffering_time
        self.loaded_fraction = loaded_fraction
        self.downloaded_bytes = downloaded_bytes

    def __repr__(self):
        return '<VideoResults, id: %r, downloaded bytes: %r, quality: %r>' % (
            self.id, self.downloaded_bytes, self.quality)
