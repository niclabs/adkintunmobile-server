from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from initial_data import initial_data

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@migrate.configure
def configure_alembic(config):
    config.compare_type = True
    return config

@manager.command
def test():
    import unittest
    testmodules = [
        'tests',
    ]

    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner(verbosity=2).run(suite)


def crazy_call():
    print("crazy_call")


@manager.command
def runserver():
    init_db()
    app.run()


def init_db():
    import json
    jsonvar = json.loads(initial_data)

if __name__ == '__main__':
    manager.run()
