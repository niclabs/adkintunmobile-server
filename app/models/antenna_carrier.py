from app import db
from sqlalchemy import PrimaryKeyConstraint

# Tabla para manejar la relacion many_to_many entre antenas y carriers
antennas_carriers = db.Table('antennas_carriers',
                             db.Column('antenna_id', db.Integer, db.ForeignKey('antennas.id')),
                             db.Column('carrier_id', db.Integer, db.ForeignKey('carriers.id')),
                             PrimaryKeyConstraint('antenna_id', 'carrier_id', name='antenna_carrier_id'),
                             )
