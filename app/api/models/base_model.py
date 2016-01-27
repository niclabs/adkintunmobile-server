from . import utils
from app import db


class BaseModel(db.Model):
    '''
    Clase modelo base.
    '''
    __abstract__  = True

    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
