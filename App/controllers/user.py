from App.models import User
from App.database import db

#make user an abstract table, make a create admin, and create student
from App.models import Admin, Student
from App.database import db

def create_user(username, password, user_type='student'):
    """
    Create a new user (Admin or Student) and save to the database.
    """
    if user_type == 'admin':
        new_user = Admin(username=username, password=password)  # Create Admin instance
    else:
        new_user = Student(username=username, password=password)  # Create Student instance
    
    db.session.add(new_user)
    db.session.commit()  # This should work without warnings if defined correctly
    return new_user




def get_user_by_username(username):
    """
    Retrieve a user by their username.
    """
    return User.query.filter_by(username=username).first()

def get_user(id):
    """
    Retrieve a user by their ID.
    """
    return User.query.get(id)

def get_all_users():
    """
    Retrieve all users (both students and admins).
    """
    return User.query.all()

def get_all_users_json():
    """
    Retrieve all users and return them as a list of JSON objects.
    """
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username=None, role=None):
    """
    Update a user's information. If username or role is provided, update accordingly.
    """
    user = get_user(id)
    if user:
        if username:
            user.username = username
        if role:  # Ensure that the role can also be updated if necessary
            user.role = role
        db.session.add(user)
        db.session.commit()
        return user
    return None

def get_users_by_role(role):
    """
    Retrieve all users by a specific role ('admin' or 'student').
    """
    return User.query.filter_by(role=role).all()

def get_username_by_id(user_id):
    """ Helper function to get username by user ID. """
    # Assuming you have a User model to fetch user details
    user = User.query.get(user_id)
    return user.username if user else "Unknown User"
