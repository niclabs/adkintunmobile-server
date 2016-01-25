from . import utils


class ModelMixin():
    '''
    Clase modelo base.
    '''
    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
