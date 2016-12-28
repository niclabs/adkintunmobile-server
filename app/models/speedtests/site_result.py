from app import db
from app.models.base_model import BaseModel


class SiteResult(BaseModel):
    '''
    Site results model class
    '''
    __tablename__ = 'site_results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    loaded = db.Column(db.Boolean)
    loading_time = db.Column(db.BigInteger)
    downloaded_bytes = db.Column(db.BigInteger)

    # relationships
    connectivity_test_report_id = db.Column(db.Integer, db.ForeingKey("connectivity_test_report.id"))

    def __init__(self, url=None, loaded=None, loaded_time=None, downloaded_bytes=None):
        self.url = url
        self.loaded = loaded
        self.loading_time = loaded_time
        self.downloaded_bytes = downloaded_bytes

    def __repr__(self):
        return '<SiteResult, id: %r, url: %r, downloaded bytes: %r>' % (self.id, self.url, self.downloaded_bytes)
