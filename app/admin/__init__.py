from app import application
from app.admin.login import init_login, MyAdminIndexView

from flask_admin import Admin

init_login()

admin = Admin(application, name='Adkintun', index_view=MyAdminIndexView(), base_template='admin/my_master.html', template_mode='bootstrap3')

from . import views

# Initialize flask-login