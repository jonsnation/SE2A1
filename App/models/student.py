from App.database import db
from App.models.user import User

class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password):
        super().__init__(username, password, user_type='student')

  