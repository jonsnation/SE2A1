from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    __tablename__ = 'user'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))  # discriminator column

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    def __init__(self, username, password, user_type=None, id=None):
        if id is not None:
            self.id = id  
        self.username = username
        self.set_password(password)
        if user_type:
            self.type = user_type 

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
