from flask import Flask, g

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

from flask_sqlalchemy import SQLAlchemy

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')

from config import AppTokens


@auth.verify_token
def verify_token(token):
    if token in AppTokens.tokens:
        g.current_user = AppTokens.tokens[token]
        return True
    return False


from . import api
from . import public
from . import admin
from . import report

from app.automatization.scheduler_manager import start_scheduler

start_scheduler()
