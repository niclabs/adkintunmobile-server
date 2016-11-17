from app import db

# Tabla para manejar la relacion many_to_many entre antenas y eventos gsm
antennas_gsm_events = db.Table('antennas_gsm_events',
                               db.Column('antenna_id', db.Integer, db.ForeignKey('antennas.id')),
                               db.Column('gsm_event_id', db.Integer, db.ForeignKey('gsm_events.id'))
                               )
