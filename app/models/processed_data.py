from app import db
from app.models import base_model


class ProcessedData(base_model.BaseModel):
    '''
    Clase de datos procesados.
    Almacena informes de los eventos registrados en el sistema hasta esa fecha
    '''

    __tablename__ = 'processed_data'
    id = db.Column(db.Integer, primary_key=True)
    total_events = db.Column(db.Integer)
    total_devices = db.Column(db.Integer)
    total_sims = db.Column(db.Integer)
    #Totales de tipos de eventos
    #Totales de eventos por carrier

    def __repr__(self):
        return '<ProcessedData %r>' % (self.id)