from app import db
from app.models import base_model


class ActiveMeasurement(base_model.BaseModel):
    """
    Active measurement model class
    """
    __tablename__ = "active_measurements"
    id = db.Column(db.Integer, primary_key=True)
    # ver como guardar en su momento
    network_interface_id = db.Column(db.Integer, db.ForeignKey("network_interfaces.id"))
    # transformar al guardar
    date = db.Column(db.DateTime)
    dispatched = db.Column(db.Boolean)

    # Herencia
    type = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_on': type}
