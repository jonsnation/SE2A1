from App.models import Result
from App.database import db

#add admin id
def add_result(competition_id, user_id, score, rank, time_taken=None, problems_solved=None):
    """
    Add a new result to a competition for a user.
    """
    result = Result(
        competition_id=competition_id,
        user_id=user_id,
        score=score,
        rank=rank,
        time_taken=time_taken,
        problems_solved=problems_solved
    )
    db.session.add(result)
    db.session.commit()
    return result

def get_result_by_id(result_id):
    """
    Retrieve a result by its ID.
    """
    return Result.query.get(result_id)

def get_results_by_competition(competition_id):
    """
    Retrieve all results for a given competition.
    """
    return Result.query.filter_by(competition_id=competition_id).all()

def get_results_by_user(user_id):
    """
    Retrieve all results for a given user.
    """
    return Result.query.filter_by(user_id=user_id).all()

def update_result(result_id, score=None, rank=None, time_taken=None, problems_solved=None):
    """
    Update a specific result's details.
    """
    result = get_result_by_id(result_id)
    if result:
        if score is not None:
            result.score = score
        if rank is not None:
            result.rank = rank
        if time_taken:
            result.time_taken = time_taken
        if problems_solved:
            result.problems_solved = problems_solved
        db.session.add(result)
        db.session.commit()
        return result
    return None

def delete_result(result_id):
    """
    Delete a result by its ID.
    """
    result = get_result_by_id(result_id)
    if result:
        db.session.delete(result)
        db.session.commit()
        return result
    return None