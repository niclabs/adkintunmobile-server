import flask_login as login
from app import db
from app.admin import admin
from app.models.antenna import Antenna
from app.models.application import Application
from app.models.carrier import Carrier
from app.models.cdma_event import CdmaEvent
from app.models.connectivity_event import ConnectivityEvent
from app.models.device import Device
from app.models.event import Event
from app.models.gsm_event import GsmEvent
from app.models.sim import Sim
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent
from flask_admin.contrib.sqla import ModelView


class StandardView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    can_delete = False
    can_create = False
    can_edit = False
    can_export = True


class EventView(StandardView):
    column_sortable_list = (
        ("sim", Sim.serial_number), ("device", Device.device_id), "id", "date", "app_version_code", "type")


class GsmEventView(StandardView):
    column_sortable_list = (
        ("sim", Sim.serial_number), ("device", Device.device_id), ("carrier", Carrier.id), "id", "date",
        "app_version_code",
        "type", "telephony_standard", "network_type", "signal_strength_size", "signal_strength_mean",
        "signal_strength_variance", "signal_ber_size", "signal_ber_mean", "signal_ber_variance", "gsm_lac", "gsm_cid",
        "gsm_psc")


# Add views
# admin.add_view(UserView(User, db.session))

admin.add_view(StandardView(Antenna, db.session))
admin.add_view(StandardView(Carrier, db.session))
admin.add_view(StandardView(Device, db.session))
admin.add_view(StandardView(Sim, db.session))
admin.add_view(StandardView(Application, db.session))

# Events
admin.add_view(EventView(Event, db.session))
admin.add_view(GsmEventView(GsmEvent, db.session))
admin.add_view(StandardView(CdmaEvent, db.session))
admin.add_view(StandardView(ConnectivityEvent, db.session))
admin.add_view(StandardView(StateChangeEvent, db.session))
admin.add_view(StandardView(TrafficEvent, db.session))
