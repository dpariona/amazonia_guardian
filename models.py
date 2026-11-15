from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='viewer') # 'admin' o 'viewer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    sensor = db.Column(db.String(10), nullable=False) # MODIS o VIIRS
    confidence = db.Column(db.String(20))
    acq_date = db.Column(db.String(20))
    frp = db.Column(db.Float)
    time = db.Column(db.String(10))
    satellite = db.Column(db.String(50))
    is_anomaly = db.Column(db.Boolean, default=False) # NUEVO CAMPO

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'sensor': self.sensor,
            'confidence': self.confidence,
            'acq_date': self.acq_date,
            'frp': self.frp,
            'time': self.time,
            'satellite': self.satellite,
            'is_anomaly': self.is_anomaly
        }