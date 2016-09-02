from app import db
from app.models import utils


class BaseModel(db.Model):
    '''
    Clase modelo base.
    '''
    __abstract__  = True

    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
