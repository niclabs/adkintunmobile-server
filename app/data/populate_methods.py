from sqlalchemy.exc import IntegrityError

from app import db
from app.data import initial_data_carriers


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


def initial_populate():
    populate_user()
    populate_carriers()
