from app import db
from app.models import base_model


class Application(base_model.BaseModel):
    """
    Android Apps model class
    """
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(100), unique=True)
    application_traffic_event = db.relationship("ApplicationTrafficEvent", backref="application", lazy="dynamic")

    def __init__(self, package_name=None):
        self.package_name = package_name

    def __repr__(self):
        return "<Application, package_name: %r, id: %r>" % (self.package_name, self.id)

    @staticmethod
    def get_app_or_add_it(packageName):
        """
        Search an app and retrieve it if exist, else create a new one and retrieve it.
        """
        app = Application.query.filter(Application.package_name == packageName).first()
        if not app:
            from app import Session
            app = Application(package_name=packageName)
            session = Session()
            session.add(app)
            session.commit()
        return app
