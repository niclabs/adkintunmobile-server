from flask.ext.migrate import Migrate, MigrateCommand

from config import AppTokens
from flask import g
from flask_script import Manager

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)


from manage_commands import Test,  PopulateAntennas, Populate

manager.add_command('db', MigrateCommand)
manager.add_command('test', Test())
manager.add_command('populate', Populate())
manager.add_command('populate_antennas', PopulateAntennas())

if __name__ == '__main__':
    manager.run()
