from app import db

# Tabla para manejar la relacion many_to_many entre antenas y carriers entre devices y simss
devices_sims = db.Table('devices_sims',
                         db.Column('device_id', db.Integer, db.ForeignKey('devices.device_id')),
                         db.Column('sim_id', db.Integer, db.ForeignKey('sims.serial_number')),
                         # db.Column('creation_date', db.Date),
                         db.Column('id', db.Integer, primary_key=True)
                         )
