from flask_restful import Api
from .. import app

# API stuff
api = Api(app)

from . import views
