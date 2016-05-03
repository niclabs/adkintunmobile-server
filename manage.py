from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Server

from app import app, db
from config import AppTokens
from flask import g
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.exc import IntegrityError
from static.data.initial_data_antennas import initial_data_antennas
from static.data.initial_data_carriers import initial_data_carriers

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
    from app.models.antenna import Antenna
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
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    # Agregar carriers
    jsonvar = json.loads(initial_data_carriers)
    for k, v in jsonvar.items():
        if k == "carriers":
            save_models(v, Carrier)

    # Agregar antennas
    jsonvar = json.loads(initial_data_antennas)
    for k, v in jsonvar.items():
        if k == "antennas":
            for json_element in v:
                antenna = Antenna()
                try:
                    mnc = json_element['mnc']
                    mcc = json_element['mcc']
                    carrier = Carrier.query.filter(Carrier.mnc == mnc and Carrier.mcc == mcc).first()
                    antenna.carriers.append(carrier)
                except KeyError:
                    continue
                for k, v in json_element.items():
                    if hasattr(antenna, k):
                        setattr(antenna, k, v)
                db.session.add(antenna)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()


def save_models(elements, model_class):
    for json_element in elements:
        model = model_class()
        for k, v in json_element.items():
            setattr(model, k, v)
        db.session.add(model)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


@auth.verify_token
def verify_token(token):
    if token in AppTokens.tokens:
        g.current_user = AppTokens.tokens[token]
        return True
    return False


@manager.command
def delete_db_test():
    # app.config.from_object('config.TestingConfig')
    db.drop_all(bind=None)


@manager.command
def populate_test():
    # app.config.from_object('config.TestingConfig')
    db.create_all()
    # devices
    from app.models.carrier import Carrier
    from app.models.device import Device
    from app.models.sim import Sim
    from app.models.gsm_event import GsmEvent

    from datetime import datetime
    from datetime import timedelta

    from config import AdminUser
    from app.models.user import User
    from werkzeug.security import generate_password_hash

    device1 = Device(device_id="1", creation_date=datetime.now() + timedelta(days=-2))
    device2 = Device(device_id="2", creation_date=datetime.now())
    device3 = Device(device_id="3", creation_date=datetime.now())
    device4 = Device(device_id="4", creation_date=datetime.now())

    # sims
    sim1 = Sim(serial_number="123", creation_date=datetime.now() + timedelta(days=-2))
    sim2 = Sim(serial_number="456", creation_date=datetime.now())
    sim3 = Sim(serial_number="789", creation_date=datetime.now())

    sim1.devices.append(device1)
    sim1.devices.append(device2)
    sim2.devices.append(device1)
    sim2.devices.append(device3)
    sim3.devices.append(device4)

    # carriers
    carrier1 = Carrier(name="Compañia 1")
    carrier2 = Carrier(name="Compañia 2")

    carrier1.sims.append(sim1)
    carrier1.sims.append(sim2)
    carrier2.sims.append(sim3)

    # GSM events
    event1 = GsmEvent(date=datetime.now() + timedelta(days=-2))
    event2 = GsmEvent(date=datetime.now())
    event3 = GsmEvent(date=datetime.now())
    event4 = GsmEvent(date=datetime.now() + timedelta(days=-2))
    event5 = GsmEvent(date=datetime.now())

    sim1.events.append(event1)
    sim1.events.append(event2)
    sim3.events.append(event3)
    sim3.events.append(event4)
    sim3.events.append(event5)

    device1.events = [event1, event2]
    device2.events = [event3]
    device3.events = [event4, event5]

    user = User()
    user.first_name = AdminUser.first_name
    user.last_name = AdminUser.last_name
    user.login = AdminUser.login
    user.email = AdminUser.email
    user.password = generate_password_hash(AdminUser.password)

    db.session.add(user)
    db.session.add(carrier1)
    db.session.add(carrier2)
    db.session.commit()

if __name__ == '__main__':
    manager.run()