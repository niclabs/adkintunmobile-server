from app import db
from app.models import base_model


class Application(base_model.BaseModel):
    '''
    Clase aplicaciones android
    '''
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(100), unique=True)
    application_traffic_event = db.relationship('ApplicationTrafficEvent', backref='application', lazy='dynamic')

    def __init__(self, package_name=None):
        self.package_name = package_name

    def __repr__(self):
        return '<Application, package_name: %r, id: %r>' % (self.package_name, self.id)

    @staticmethod
    def store_if_not_exist(packageName):
        application = Application.query.filter(Application.package_name == packageName).first()
        if not application:
            application = Application(package_name=packageName)
            db.session.add(application)
        return application