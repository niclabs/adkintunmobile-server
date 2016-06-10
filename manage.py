from flask.ext.migrate import Migrate, MigrateCommand

from config import AppTokens
from flask import g
from flask_script import Manager

from app import app, db

from flask_httpauth import HTTPTokenAuth


migrate = Migrate(app, db)
manager = Manager(app)
auth = HTTPTokenAuth(scheme='Token')


from manage_commands import Test,  PopulateAntennas, Populate

manager.add_command('db', MigrateCommand)
manager.add_command('test', Test())
manager.add_command('populate', Populate())
manager.add_command('populate_antennas', PopulateAntennas())


@auth.verify_token
def verify_token(token):
    if token in AppTokens.tokens:
        g.current_user = AppTokens.tokens[token]
        return True
    return False


if __name__ == '__main__':
    manager.run()
