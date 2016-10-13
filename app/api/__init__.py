from app import application
from flask_restful import Api

# API stuff

api = Api(application)
application.config['BUNDLE_ERRORS'] = True
from app.api import events_view, antennas_view


