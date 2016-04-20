from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Server

from app import app, db
from config import AppTokens
from flask import g
from flask_httpauth import HTTPTokenAuth
from initial_data import initial_data

migrate = Migrate(app, db)
manager = Manager(app)
auth = HTTPTokenAuth(scheme='Token')

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


@manager.command
def populate():
    import json
    from app.models.carrier import Carrier
    from config import AdminUser
    from app.models.user import User
    from werkzeug.security import generate_password_hash

    user = User()
    user.first_name = AdminUser.first_name
    user.last_name = AdminUser.last_name
    user.login = AdminUser.login
    user.email = AdminUser.email
    user.password = generate_password_hash(AdminUser.password)
    db.session.add(user)
    
    jsonvar = json.loads(initial_data)
    for k, v in jsonvar.items():
        if k == "carriers":
            save_models(v, Carrier)



def save_models(carriers, model_class):
    for json_carrier in carriers:
        model = model_class()
        for k, v in json_carrier.items():
            setattr(model, k, v)
        db.session.add(model)
        db.session.commit()


if __name__ == '__main__':
    manager.run()


@auth.verify_token
def verify_token(token):
    if token in AppTokens.tokens:
        g.current_user = AppTokens.tokens[token]
        return True
    return False
