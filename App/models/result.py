from App.database import db

class Result(db.Model):
    __tablename__ = 'result'  
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    score = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.String(20), nullable=True)
    problems_solved = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', backref='results', lazy=True)
    competition = db.relationship('Competition', back_populates='results', lazy=True)

    def __init__(self, competition_id, user_id, score, rank, time_taken=None, problems_solved=None):
        self.competition_id = competition_id
        self.user_id = user_id
        self.score = score
        self.rank = rank
        self.time_taken = time_taken
        self.problems_solved = problems_solved

    def get_json(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'competition_name': self.competition.name if self.competition else None,
            'user_id': self.user_id,
            'score': self.score,
            'rank': self.rank,
            'time_taken': self.time_taken,
            'problems_solved': self.problems_solved
        }
