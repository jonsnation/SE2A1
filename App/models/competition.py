from App.database import db
from datetime import datetime, timezone

class Competition(db.Model):
    __tablename__ = 'competition' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

    results = db.relationship('Result', back_populates='competition', lazy=True)

    def __init__(self, name, admin_id, description=None, date=None):
        self.name = name
        self.admin_id = admin_id
        self.description = description
        self.date = date if date else datetime.now(timezone.utc)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d'),
            'description': self.description,
            'admin_id': self.admin_id,  # Include admin ID (creator)
            'results': [result.get_json() for result in self.results]
        }
