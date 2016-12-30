from app import db
from app.models.speedtests.active_measurement import ActiveMeasurement


class ConnectivityTestReport(ActiveMeasurement):
    '''
    Connectivity test reports model class
    '''
    __tablename__ = "connectivity_test_reports"

    id = db.Column(db.Integer, db.ForeignKey("active_measurements.id"), primary_key=True)

    # Relationships
    sites_results = db.relationship("SiteResult", backref="connectivity_test_report", lazy="dynamic")

    def __init__(self, network_interface_id=None, date=None, dispatched=None):
        self.network_interface_id = network_interface_id
        self.date = date
        self.dispatched = dispatched

    def __repr__(self):
        return '<ConnectivityTestReport, id: %r, date: %r>' % (self.id, self.date)
