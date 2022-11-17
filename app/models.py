from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login  import UserMixin

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    predictions = db.relationship('Prediction', backref = 'user', lazy = 'dynamic')
    goleador = db.relationship('Goleador', backref = 'user', lazy = 'dynamic')
    # group_predictions = db.relationship('Group', backref = 'user', lazy = 'dynamic')
    
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
    pred_id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, index=True)
    team1 = db.Column(db.String(3))
    team2 = db.Column(db.String(3))
    goals1 = db.Column(db.Integer)
    goals2 = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    stage = db.Column(db.String(16))
    points_outcome = db.Column(db.Integer)
    points_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    def __repr__(self) -> str:
        return f'<Game {self.game_id} Prediction: {self.team1} {self.goals1} - {self.goals2} {self.team2}, {self.winner} wins>'

class Goleador(db.Model):
    goleador_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    prediction = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True)
    
    def __repr__(self) -> str:
        return f'{self.prediction}'
    
class Stage(db.Model):
    stage_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    stage_type = db.Column(db.String(32))
    name = db.Column(db.String(32)) # A, B, C...
    winner = db.Column(db.String(3))
    runner_up = db.Column(db.String(3))
    pts_winner_outcome = db.Column(db.Integer)
    pts_runner_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    teams = db.relationship('Team', backref = 'stage', lazy = 'dynamic', cascade="all,delete, delete-orphan",)
    
    def get_predictions_results(self, user_id, save_results = True):
        points_win = 3
        points_tie = 1
        for team in self.teams:
            team.points = 0
            team.goals_scored = 0
            team.goal_difference = 0
            
        predictions = Prediction.query.filter_by(user_id = user_id)
        for game_id in GAMES_IN_GROUP[self.name]:
            prediction = predictions.filter_by(game_id = game_id).first()
            # Get teams to assign points to
            team1 = self.teams.filter_by(country_code = prediction.team1).first()
            team2 = self.teams.filter_by(country_code = prediction.team2).first()
            
            # document team goals
            team1.goals_scored += prediction.goals1
            team2.goals_scored += prediction.goals2
            team1.goal_difference += prediction.goals1 - prediction.goals2
            team2.goal_difference += prediction.goals2 - prediction.goals1
            
            # Determine game result
            if prediction.goals1 > prediction.goals2: # Team 1 wins
                team1.points += points_win
            elif prediction.goals1 < prediction.goals2: # Team 2 wins
                team2.points += points_win
            else: # Tie
                team1.points += points_tie
                team2.points += points_tie
            
        if save_results:      
            try:
                db.session.commit()
                print("Calculated game outcomes successully")
            except:
                db.session.rollback()
                print("DID NOT calculate game outcomes successully. Session rolled back")
        else: 
            db.session.flush()

    
class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(64))
    country_code = db.Column(db.String(3))
    points = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    goal_difference = db.Column(db.Integer)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.stage_id'))
    


GROUPS = {
    'A':['QAT','ECU','SEN','NED'],
    'B':['ENG','IRN','USA','WAL'],
    'C':['ARG','KSA','MEX','POL'],
    'D':['FRA','AUS','DEN','TUN'],
    'E':['ESP','CRC','GER','JPN'],
    'F':['BEL','CAN','MAR','CRO'],
    'G':['BRA','SRB','SUI','CMR'],
    'H':['POR','GHA','URU','KOR'],
}

GAMES_IN_GROUP = {
    'A': [1, 2, 18, 19, 35, 36],
    'B': [3, 4, 17, 20, 33, 34],
    'C': [7, 8, 22, 24, 39, 40],
    'D': [5, 6, 21, 23, 37, 38],
    'E': [10, 11, 25, 28, 43, 44],
    'F': [9, 12, 26, 27, 41, 42],
    'G': [13, 16, 29, 31, 47, 48],
    'H': [14, 15, 30, 32, 45, 46]
 }

TEAM_NAMES = {
    'ARG' : 'Argentina',
    'AUS' : 'Australia',
    'BEL' : 'Belgium',
    'BRA' : 'Brazil',
    'CMR' : 'Cameroon',
    'CAN' : 'Canada',
    'CRC' : 'Costa Rica',
    'CRO' : 'Croatia',
    'DEN' : 'Denmark',
    'ECU' : 'Ecuador',
    'ENG' : 'England',
    'FRA' : 'France',
    'GER' : 'Germany',
    'GHA' : 'Ghana',
    'IRN' : 'Iran',
    'JPN' : 'Japan',
    'MEX' : 'Mexico',
    'MAR' : 'Morocco',
    'NED' : 'Netherlands',
    'POL' : 'Poland',
    'POR' : 'Portugal',
    'QAT' : 'Qatar',
    'KSA' : 'Saudi Arabia',
    'SEN' : 'Senegal',
    'SRB' : 'Serbia',
    'KOR' : 'South Korea',
    'ESP' : 'Spain',
    'SUI' : 'Switzerland',
    'TUN' : 'Tunisia',
    'URU' : 'Uruguay',
    'USA' : 'USA',
    'WAL' : 'Wales',
}