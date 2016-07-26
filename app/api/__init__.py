from app import app
from flask_restful import Api

# API stuff

api = Api(app)
app.config['BUNDLE_ERRORS'] = True
from . import events_view
