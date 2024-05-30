from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class CurrencyRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    description = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<CurrencyRate {self.currency}: {self.rate}>'
