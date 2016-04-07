from flask import Flask
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db

Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(threaded=True))

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


if __name__ == '__main__':
    manager.run()
