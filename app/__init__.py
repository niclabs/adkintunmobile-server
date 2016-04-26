from flask import Flask

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

from flask_sqlalchemy import SQLAlchemy

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from . import api
from . import public
from . import admin
from . import report

from app.automatization.scheduler_manager import start_scheduler

start_scheduler()
