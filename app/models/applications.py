from sqlalchemy import Column, Integer, String
from . import base_model


class Application(base_model.BaseModel):
    '''
    Clase aplicaciones android
    '''
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    package_name = Column(String(100), unique=True)

    def __init__(self, package_name):
        self.package_name = package_name

    def __repr__(self):
        return '<Application, package_name: %r, id: %r>' % (self.package_name, self.id)
