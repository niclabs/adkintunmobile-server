from app.models.sim import Sim
from app.models.carrier import Carrier
from app.models.device import Device

from flask_admin.contrib.sqla import ModelView
from . import admin
from app import db


class SimView(ModelView):
    column_display_pk = True
    create_modal = True

class CarrierView(ModelView):
    column_display_pk = True
    create_modal = True
    column_exclude_list = ['id', ]

class DeviceView(ModelView):
     column_display_pk = True
     # column_hide_backrefs = False
     # column_list = ('id', 'sdk', 'mobile_plan')

# class AntennaView(sqla.ModelView):
#     pass

# Add views
# admin.add_view(UserView(User, db.session))
admin.add_view(DeviceView(Device, db.session))
# admin.add_view(sqla.ModelView(Antenna, db.session))
admin.add_view(SimView(Sim, db.session))
# admin.add_view(sqla.ModelView(Mobile_Plan, db.session))
admin.add_view(CarrierView(Carrier, db.session))
