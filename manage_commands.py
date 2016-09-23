from flask_script import Command, Option
from sqlalchemy.exc import IntegrityError

from app import db
from app.data import initial_data_carriers


class Geolocalization(Command):
    option_list = (
        Option('--antennas', '-a', dest='antennas'),
    )

    def run(self, antennas=1000):
        from app.data.antennas_geolocalization import update_antennas_localization

        geolocalizated_antennas = update_antennas_localization(max_number_of_queries=antennas)
        print("Geolocalizated antennas:" + str(geolocalizated_antennas))


class Test(Command):
    def run(self):
        import unittest
        testmodules = [
            "tests",
        ]

        suite = unittest.TestSuite()

        for t in testmodules:
            try:
                # If the module defines a suite() function, call it to get the suite.
                mod = __import__(t, globals(), locals(), ["suite"])
                suitefn = getattr(mod, "suite")
                suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

        unittest.TextTestRunner(verbosity=2).run(suite)


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


class Populate(Command):
    def run(self):
        populate()


def populate():
    populate_user()
    populate_carriers()


def populate_user():
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


def populate_carriers():
    import json
    from app.models.carrier import Carrier
    jsonvar = json.loads(initial_data_carriers.initial_data_carriers)
    for k, v in jsonvar.items():
        if k == "carriers":
            save_models(v, Carrier)


def delete_db():
    db.drop_all(bind=None)


def populate_test():
    from app.models.antenna import Antenna
    from app.models.carrier import Carrier
    populate_carriers()
    antenna1 = Antenna(cid=1259355, lac=55700, lat=0.2, lon=0.1)
    antenna2 = Antenna(cid=1277982, lac=55700, lat=0.3, lon=0.4)
    carrier = Carrier.query.filter(Carrier.mnc == 2 and Carrier.mcc == 730).first()
    carrier.antennas.append(antenna1)
    carrier.antennas.append(antenna2)
    db.session.add(antenna1)
    db.session.add(antenna2)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
