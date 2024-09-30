from App.models import Competition, User
from App.database import db
from datetime import datetime

def create_competition(name, description=None, date=None, admin_id=None):
    existing_competition = Competition.query.filter_by(name=name).first()
    if existing_competition:
        return None 

    
    admin = User.query.get(admin_id)
    
    
    if not admin or admin.type != 'admin':  
        return None  

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
    competition = Competition.query.get(competition_id)
    if not competition:
        return None

    if name:
        competition.name = name
    if description:
        competition.description = description
    if date:
        
        competition.date = datetime.strptime(date, '%Y-%m-%d')  

    db.session.commit()
    return competition


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
