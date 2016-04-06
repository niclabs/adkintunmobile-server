from app import db
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.event import Event
from app.models.sim import Sim
from flask_admin.contrib.sqla import ModelView
from . import admin


class SimView(ModelView):
    column_display_pk = True
    create_modal = True


class CarrierView(ModelView):
    column_display_pk = True
    create_modal = True
    column_exclude_list = ['id', ]


class DeviceView(ModelView):
    column_display_pk = True
    create_modal = True
    # column_hide_backrefs = False
    # column_list = ('id', 'sdk', 'mobile_plan')

class EventView(ModelView):
    column_display_pk = True
    create_modal = True


# class AntennaView(sqla.ModelView):
#     pass

# Add views
# admin.add_view(UserView(User, db.session))
admin.add_view(DeviceView(Device, db.session))
# admin.add_view(sqla.ModelView(Antenna, db.session))
admin.add_view(SimView(Sim, db.session))
# admin.add_view(sqla.ModelView(Mobile_Plan, db.session))
admin.add_view(CarrierView(Carrier, db.session))
admin.add_view(EventView(Event, db.session))
