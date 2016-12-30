from app import db, application
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
    connectivity_test_report_id = db.Column(db.Integer, db.ForeignKey("connectivity_test_reports.id"))

    def __init__(self, url=None, loaded=None, loading_time=None, downloaded_bytes=None):
        self.url = url
        self.loaded = loaded
        self.loading_time = loading_time
        self.downloaded_bytes = downloaded_bytes

    def __repr__(self):
        return '<SiteResult, id: %r, url: %r, downloaded bytes: %r>' % (self.id, self.url, self.downloaded_bytes)

    @staticmethod
    def add_site_result(args: dict):
        """
        Create a new site result object from a dict
        :param args: dict with site result data
        :return: Site result object
        """
        if "url" in args and "loading_time" in args and "downloaded_bytes" in args and "loaded" in args:
            sr = SiteResult(url=args["url"], loading_time=args["loading_time"],
                            downloaded_bytes=args["downloaded_bytes"], loaded=args["loaded"])
            db.session.add(sr)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                application.logger.error("Error adding site result, url:" + args["url"])
                return None
            return sr
        else:
            return None
