from app import db
from sqlalchemy import PrimaryKeyConstraint

# Table to manage many to many relationship between device and sims
devices_sims = db.Table('devices_sims',
                        db.Column('device_id', db.String(50), db.ForeignKey('devices.device_id')),
                        db.Column('sim_id', db.String(50), db.ForeignKey('sims.serial_number')),
                        PrimaryKeyConstraint('device_id', 'sim_id', name='device_sim_id'),
                        )
