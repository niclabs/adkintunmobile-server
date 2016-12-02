import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, g
from flask_autoindex import AutoIndex
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from config import AppTokens, Files

# Create flask app
application = Flask(__name__)

# Load the default configuration
application.config.from_object("config.DefaultConfig")

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(application)

# Authetication scheme
auth = HTTPTokenAuth(scheme="Token")

# Listing reports directory
autoindex = AutoIndex(application, browse_root=Files.REPORTS_FOLDER, add_url_rules=False)


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
if not application.debug:
    log_folder = Files.LOGS_FOLDER
    log_filename = Files.PRINCIPAL_LOG_FILE
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    file_handler = RotatingFileHandler(log_folder + "/" + log_filename, maxBytes=50 * 1024 * 1024)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    application.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.info("Adkintun log start")

# start uwsgi cron jobs for antennas geolocalization and reports generation
# Just run in a uwsgi instance!
try:
    import app.automatization.scheduler_manager

    application.logger.info("Uwsgi mules created for antennas geolocalization and reports generation")
except:
    application.logger.error("Problem with the mules")
