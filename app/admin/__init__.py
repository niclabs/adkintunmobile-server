from .. import app
from flask_admin import Admin


admin = Admin(app, name='Adkintun', template_mode='bootstrap3')

from . import views
