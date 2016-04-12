import flask_login as login
from flask import render_template
from flask_admin.contrib.sqla import ModelView

from app import db
from app.admin import admin
from app.models.carrier import Carrier
from app.models.device import Device
from app.models.event import Event
from app.models.sim import Sim
from .. import app


# Flask views
@app.route('/')
def index():
    return render_template('index.html')

class SimView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    create_modal = True


class CarrierView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    create_modal = True
    column_exclude_list = ['id', ]


class DeviceView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    create_modal = True
    # column_hide_backrefs = False
    # column_list = ('id', 'sdk', 'mobile_plan')

class EventView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

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
