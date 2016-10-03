import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, g
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from config import AppTokens


# Create flask app
app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DefaultConfig')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Authetication scheme
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    Verify token for authentication
    :param token: Token used by client
    :return: Boolean
    """

    if token in AppTokens.tokens:
        g.current_user = AppTokens.tokens[token]
        return True
    return False


from app import api
from app import public
from app import admin
from app import report


# Create log files
if not app.debug:
    log_folder = 'tmp/'
    log_filename = 'adkintun-error.log'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    file_handler = RotatingFileHandler(log_folder + log_filename, 'a', maxBytes=50 * 1024 * 1024)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Adkintun log start')

# start uwsgi cron jobs for antennas geolocalization and reports generation
# Just run in a uwsgi instance!
try:
    import app.automatization.scheduler_manager
except:
    pass