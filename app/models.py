from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login  import UserMixin

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    predictions = db.relationship('Prediction', backref = 'user', lazy = 'dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_id(self):
           return (self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key = True)
    utc_time = db.Column(db.DateTime, index = True)
    team1 = db.Column(db.String(3))
    team2 = db.Column(db.String(3))
    group = db.Column(db.String(1))
    location = db.Column(db.String(120))
    stage = db.Column(db.String(16))
    cell1 = db.Column(db.String(4))
    cell2 = db.Column(db.String(4))
    
        
    def __repr__(self) -> str:
        return f'<{self.stage} stage game on {self.utc_time} | {self.game_id}: {self.team1} v. {self.team2}>'
    
class Prediction(db.Model):
    pred_id = db.Column(db.String(5), primary_key = True)
    game_id = db.Column(db.Integer, index=True)
    team1 = db.Column(db.String(3))
    team2 = db.Column(db.String(3))
    goals1 = db.Column(db.Integer)
    goals2 = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    def __repr__(self) -> str:
        return f'<Game {self.game_id} Prediction: {self.team1} {self.goals1} - {self.goals2} {self.team2}, {self.winner} wins>'

