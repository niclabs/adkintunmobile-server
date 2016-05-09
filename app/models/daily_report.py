from app import db


class DailyReport(db.Model):
    __tablename__ = 'daily_reports'
    id = db.Column(db.Integer, primary_key=True)
    total_devices = db.Column(db.Integer)
    total_sims = db.Column(db.Integer)
    total_events = db.Column(db.Integer)
    devices_none = db.Column(db.Integer)
    devices_entel = db.Column(db.Integer)
    devices_movistar = db.Column(db.Integer)
    devices_claro = db.Column(db.Integer)
    devices_wom = db.Column(db.Integer)
    devices_tds = db.Column(db.Integer)
    devices_vtrm = db.Column(db.Integer)
    devices_ccwm = db.Column(db.Integer)
    devices_virginm = db.Column(db.Integer)
    devices_will = db.Column(db.Integer)
    sims_none = db.Column(db.Integer)
    sims_entel = db.Column(db.Integer)
    sims_movistar = db.Column(db.Integer)
    sims_claro = db.Column(db.Integer)
    sims_wom = db.Column(db.Integer)
    sims_tds = db.Column(db.Integer)
    sims_vtrm = db.Column(db.Integer)
    sims_ccwm = db.Column(db.Integer)
    sims_virginm = db.Column(db.Integer)
    sims_will = db.Column(db.Integer)
    events_none = db.Column(db.Integer)
    events_entel = db.Column(db.Integer)
    events_movistar = db.Column(db.Integer)
    events_claro = db.Column(db.Integer)
    events_wom = db.Column(db.Integer)
    events_tds = db.Column(db.Integer)
    events_vtrm = db.Column(db.Integer)
    events_ccwm = db.Column(db.Integer)
    events_virginm = db.Column(db.Integer)
    events_will = db.Column(db.Integer)

    def __init__(self, total_devices=0, total_sims=0, total_events=0, devices_none=0, devices_entel=0,
                 devices_movistar=0, devices_claro=0, devices_wom=0, devices_tds=0, devices_vtrm=0, devices_ccwm=0,
                 devices_virginm=0, devices_will=0, sims_none=0, sims_entel=0, sims_movistar=0, sims_claro=0,
                 sims_wom=0, sims_tds=0, sims_vtrm=0, sims_ccwm=0, sims_virginm=0, sims_will=0, events_none=0,
                 events_entel=0, events_movistar=0, events_claro=0, events_wom=0, events_tds=0, events_vtrm=0,
                 events_ccwm=0, events_virginm=0, events_will=0):

        self.total_devices = total_devices
        self.total_sims = total_sims
        self.total_events = total_events
        self.devices_none = devices_none
        self.devices_entel = devices_entel
        self.devices_movistar = devices_movistar
        self.devices_claro = devices_claro
        self.devices_wom = devices_wom
        self.devices_tds = devices_tds
        self.devices_vtrm = devices_vtrm
        self.devices_ccwm = devices_ccwm
        self.devices_virginm = devices_virginm
        self.devices_will = devices_will
        self.sims_none = sims_none
        self.sims_entel = sims_entel
        self.sims_movistar = sims_movistar
        self.sims_claro = sims_claro
        self.sims_wom = sims_wom
        self.sims_tds = sims_tds
        self.sims_vtrm = sims_vtrm
        self.sims_ccwm = sims_ccwm
        self.sims_virginm = sims_virginm
        self.sims_will = sims_will
        self.events_none = events_none
        self.events_entel = events_entel
        self.events_movistar = events_movistar
        self.events_claro = events_claro
        self.events_wom = events_wom
        self.events_tds = events_tds
        self.events_vtrm = events_vtrm
        self.events_ccwm = events_ccwm
        self.events_virginm = events_virginm
        self.events_will = events_will
