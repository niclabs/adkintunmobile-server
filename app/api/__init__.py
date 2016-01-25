from .. import app
from flask_restful import Api


# API stuff
api = Api(app)

from . import models
from . import views
