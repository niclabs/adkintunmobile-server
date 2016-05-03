from app import db

class DailyReport(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))
    count_devices = db.Column(db.Integer)
    count_sims = db.Column(db.Integer)
    count_events = db.Column(db.Integer)

    def __init__(self, count_devices=0, count_sims=0, count_events=0):
        self.count_devices = count_devices
        self.count_sims = count_sims
        self.count_events = count_events