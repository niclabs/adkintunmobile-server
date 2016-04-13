from app import app
from app.admin.login import MyAdminIndexView, init_login

from flask_admin import Admin

admin = Admin(app, name='Adkintun', index_view=MyAdminIndexView(), base_template='my_master.html')
# Initialize flask-login
init_login()

from . import views
