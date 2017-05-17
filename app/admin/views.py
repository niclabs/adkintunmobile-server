import flask_login as login
from flask_admin.contrib.sqla import ModelView

from app import db
from app.admin import admin
from app.models.antenna import Antenna
from app.models.application import Application
from app.models.application_traffic_event import ApplicationTrafficEvent
from app.models.carrier import Carrier
from app.models.cdma_event import CdmaEvent
from app.models.connectivity_event import ConnectivityEvent
from app.models.device import Device
from app.models.event import Event
from app.models.gsm_event import GsmEvent
from app.models.sim import Sim
from app.models.state_change_event import StateChangeEvent
from app.models.traffic_event import TrafficEvent


class StandardView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    can_delete = False
    can_create = False
    can_edit = False
    can_export = True


class AntennaView(StandardView):
    column_sortable_list = ("id", "cid", "lac", "lat", "lon", ("carrier", "carrier.id"))


class EventView(StandardView):
    column_sortable_list = (
        ("sim", "sim.serial_number"), ("device", "device.device_id"), "id", "date", "app_version_code")


class GsmEventView(StandardView):
    column_sortable_list = (
        ("sim", "sim.serial_number"), ("device", "device.device_id"), ("carrier", "carrier_id"),
        ("antenna", "antenna.id"), "id", "date", "app_version_code", "telephony_standard", "network_type",
        "signal_strength_size", "signal_strength_mean", "signal_strength_variance", "signal_ber_size",
        "signal_ber_mean", "signal_ber_variance", "gsm_psc", "mnc", "mcc", "gsm_lac", "gsm_cid")


class SimView(StandardView):
    column_sortable_list = ("serial_number", "creation_date", ("carrier", "carrier.id"))


class ConnectivityEventView(StandardView):
    column_sortable_list = (
        "date", "app_version_code", "detailed_state", "available", "connected", "roaming", "connection_type",
        "connection_type_other", ("sim", "sim.serial_number"), ("device", "device.device_id"))


class StateChangeEventView(StandardView):
    column_sortable_list = (
        "date", "app_version_code", "state_type", "state", "event_type", ("sim", "sim.serial_number"),
        ("device", "device.device_id"))


class TrafficEventView(StandardView):
    column_sortable_list = (
        "date", "app_version_code", "network_type", "rx_bytes", "tx_bytes", "rx_packets", "tx_packets",
        "tcp_rx_bytes", "tcp_tx_bytes", ("sim", "sim.serial_number"),
        ("device", "device.device_id"))

class ApplicationTrafficEventView(StandardView):
    column_sortable_list = (
        "date", "app_version_code", "network_type", "rx_bytes", "tx_bytes", "rx_packets", "tx_packets",
        "tcp_rx_bytes", "tcp_tx_bytes", ("sim", "sim.serial_number"), ("application", "application.id" ),
        ("device", "device.device_id"))

# Add views
# admin.add_view(UserView(User, db.session))

admin.add_view(AntennaView(Antenna, db.session))
admin.add_view(StandardView(Carrier, db.session))
admin.add_view(StandardView(Device, db.session))
admin.add_view(SimView(Sim, db.session))
admin.add_view(StandardView(Application, db.session))

# Events
admin.add_view(EventView(Event, db.session))
admin.add_view(GsmEventView(GsmEvent, db.session))
admin.add_view(StandardView(CdmaEvent, db.session))
admin.add_view(ConnectivityEventView(ConnectivityEvent, db.session))
admin.add_view(StateChangeEventView(StateChangeEvent, db.session))
admin.add_view(TrafficEventView(TrafficEvent, db.session))
admin.add_view(ApplicationTrafficEventView(ApplicationTrafficEvent, db.session))
