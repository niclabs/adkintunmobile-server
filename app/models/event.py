from app import db
from app.models.base_model import BaseModel


class Event(BaseModel):
    '''
    Clase Eventos, base de todos los eventos
    '''
    __tablename__ = 'events'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    app_version_code = db.Column(db.String(10))
    date = db.Column(db.Date())

