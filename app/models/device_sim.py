from app import db

# Tabla para manejar la relacion many_to_many entre antenas y carriers entre devices y sims
devices_sims = db.Table('devices_sims',
                         db.Column('device_id', db.String(50), db.ForeignKey('devices.device_id')),
                         db.Column('sim_id', db.String(50), db.ForeignKey('sims.serial_number')),
                         db.Column('id', db.Integer, primary_key=True)
                         )
