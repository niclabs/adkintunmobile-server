from app import db
from app.models.speedtests.active_measurement import ActiveMeasurement


class SpeedTestReport(ActiveMeasurement):
    '''
    Media test reports model class
    '''
    __tablename__ = "speed_test_reports"

    id = db.Column(db.Integer, db.ForeignKey("active_measurements.id"), primary_key=True)
    host = db.Column(db.String(100))
    upload_size = db.Column(db.BigInteger)
    download_size = db.Column(db.BigInteger)
    upload_speed = db.Column(db.Float)
    download_speed = db.Column(db.Float)
    elapsed_upload_time = db.Column(db.BigInteger)
    elapsed_download_time = db.Column(db.BigInteger)

    def __init__(self, network_interface_id=None, date=None, dispatched=None, video_id=None, host=None,
                 upload_size=None, download_size=None, upload_speed=None, download_speed=None, elapsed_upload_time=None,
                 elapsed_download_time=None):
        self.network_interface_id = network_interface_id
        self.date = date
        self.dispatched = dispatched
        self.video_id = video_id
        self.host = host
        self.upload_size = upload_size
        self.download_size = download_size
        self.upload_speed = upload_speed
        self.download_speed = download_speed
        self.elapsed_upload_time = elapsed_upload_time
        self.elapsed_download_time = elapsed_download_time

    def __repr__(self):
        return '<SpeedTestReport, id: %r, date: %r>' % (self.id, self.date)
