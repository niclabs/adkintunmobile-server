from app import db
from app.models import base_model


class Sample(base_model.BaseModel):
    '''
    Clase sample
    '''
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    mean = db.Column(db.Float)
    variance = db.Column(db.Float)

    def __init__(self, size, mean, variance):
        self.size = size
        self.mean = mean
        self.variance = variance

    def __repr__(self):
        return '<Sample, id: %r, size: %r, mean: %r, variance: %r>' % (self.id, self.size, self.mean, self.variances)
