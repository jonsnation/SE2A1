from App.models import Competition, User
from App.database import db

# Competition Controllers
def create_competition(name, description=None, date=None, admin_id=None):
    # Check if a competition with the same name already exists
    existing_competition = Competition.query.filter_by(name=name).first()
    if existing_competition:
        return None  # Return None to signal competition with the same name exists

    # Verify if admin_id exists and corresponds to an Admin user
    admin = User.query.get(admin_id)
    
    # Assuming `User` has a polymorphic `type` or `user_type` field
    if not admin or admin.type != 'admin':  # Adjust 'type' to whatever your discriminator is called
        return None  # Return None to signal invalid or non-admin user

    new_competition = Competition(
        name=name,
        description=description,
        date=date,
        admin_id=admin_id
    )
    db.session.add(new_competition)
    db.session.commit()
    return new_competition


def get_competition_by_id(competition_id):
    """
    Retrieve a competition by its ID.
    """
    return Competition.query.get(competition_id)

def get_all_competitions():
    """
    Retrieve all competitions from the database.
    """
    return Competition.query.all()

def get_all_competitions_json():
    """
    Retrieve all competitions and return as JSON.
    """
    competitions = get_all_competitions()
    return [competition.get_json() for competition in competitions]

def update_competition(competition_id, name=None, description=None, date=None):
    """
    Update competition details (name, description, date).
    """
    competition = get_competition_by_id(competition_id)
    if competition:
        if name:
            competition.name = name
        if description:
            competition.description = description
        if date:
            competition.date = date
        db.session.commit()  # No need to add again, just commit the changes
        return competition
    return None

def delete_competition(competition_id):
    """
    Delete a competition by its ID.
    """
    competition = get_competition_by_id(competition_id)
    if competition:
        db.session.delete(competition)
        db.session.commit()
        return competition
    return None
