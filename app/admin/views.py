from .. import db
from . import admin
from flask_admin.contrib import sqla
from app.api.models.antenna import Antenna
from app.api.models.device import Device
from app.api.models.carrier import Carrier
from app.api.models.sim import Sim


class SimView(sqla.ModelView):
    column_display_pk = True

# class DeviceView(sqla.ModelView):
#     column_display_pk = True
#     column_hide_backrefs = False
#     column_list = ('id', 'sdk', 'mobile_plan')

# class AntennaView(sqla.ModelView):
#     pass

# Add views
# admin.add_view(UserView(User, db.session))
# admin.add_view(DeviceView(Device, db.session))
# admin.add_view(sqla.ModelView(Antenna, db.session))
admin.add_view(SimView(Sim, db.session))
# admin.add_view(sqla.ModelView(Mobile_Plan, db.session))
