from flask_restful import Api

from .. import app

# API stuff
api = Api(app)
app.config['BUNDLE_ERRORS'] = True
from . import registration_view
from . import events_view
