from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from flask_login  import UserMixin
import numpy as np
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    predictions = db.relationship('Prediction', backref = 'user', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    goleador = db.relationship('Goleador', backref = 'user', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    stages = db.relationship('Stage', backref = 'user', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    events = db.relationship('EventTracker', backref = 'user', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    points = db.relationship('Points', backref = 'user', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_id(self):
           return (self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_points(self, event_description = '2022_quiniela_qatar'):
        # get points from Predictions
        if Points.query.filter_by(user_id = self.user_id).first() is not None:
            Points.query.filter_by(user_id = self.user_id).delete()
            
        pred_points= Prediction.query.filter_by(user_id = self.user_id)
        pred_points = np.array([p.points_outcome + p.points_score if p.points_outcome is not None else 0 for p in self.predictions])
        pred_sum = pred_points.sum()
        print('pred_sum',type(pred_sum))
        
        goleador_points = self.goleador.first().goleador_points if self.goleador.first().goleador_points is not None else 0
        print(goleador_points)
        
        stage_points = np.array([p.pts_winner_outcome  + p.pts_runner_score if p.pts_winner_outcome is not None else 0 for p in self.stages])
        stage_sum = stage_points.sum()
        print('stage_sum', type(np.uint32(stage_sum).item()))
        
        total_points = np.sum([pred_sum, goleador_points, stage_sum])
        points = Points(user_id = self.user_id, 
                        points = int(total_points), 
                        event_description = event_description,
                        prediction_points = np.uint32(pred_sum).item(),
                        stage_points = np.uint32(stage_sum).item(),
                        goleador_points = goleador_points)
        db.session.add(points)
        
        try:
            db.session.commit()
            print(f'{self.username} - POINTS update was successful')
            return True
        
        except Exception as e:
            db.session.rollback()
            print(f'{self.username} - POINTS update was NOT successful: {e}')
            flash(f'{self.username} - POINTS update was NOT successful: {e}', 'danger')
            return False
        
    
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key = True)
    local_time = db.Column(db.DateTime, index = True)
    team1 = db.Column(db.String(3))
    team2 = db.Column(db.String(3))
    group = db.Column(db.String(16))
    location = db.Column(db.String(120))
    stage = db.Column(db.String(16))
    official_goals1 = db.Column(db.Integer)
    official_goals2 = db.Column(db.Integer)
    round_order = db.Column(db.Integer)
    
    def __repr__(self) -> str:
        return f'< {self.game_id}: {self.team1} v. {self.team2} | {self.local_time}>'
    
    def get_average_goal_prediction(self):
        """get average goals predicted for this game"""
        goals1_avg = np.float128(db.session.query(func.avg(Prediction.goals1).label('average')).filter(Prediction.game_id == self.game_id).first()[0])
        goals2_avg = np.float128(db.session.query(func.avg(Prediction.goals2).label('average')).filter(Prediction.game_id == self.game_id).first()[0])
        return goals1_avg, goals2_avg 
    
    def get_winner(self):
        if self.official_goals1 > self.official_goals2: return self.team1
        elif self.official_goals1 < self.official_goals2: return self.team2
        else: return 'tie'  
        
    def calculate_user_points(self, user_id=None):
        if user_id is None: users = User.query.all()
        else: users = User.query.filter_by(user_id = user_id).all()
        
        official_winner = self.get_winner()
        
        for u in users:
            prediction = u.predictions.filter_by(game_id = self.game_id).first()
            if prediction is None:
                continue
            
            if self.team1 == prediction.team1 and self.team2 == prediction.team2:
                # check if score matches
                print(f'Official ({u.username}): {self.official_goals1}-{self.official_goals2} | Prediction: {prediction.goals1}-{prediction.goals2}')
                if self.official_goals1 == prediction.goals1:
                    if self.official_goals2 == prediction.goals2:
                        
                        prediction.points_score = POINT_SYSTEM[self.stage]['match_score']
                        prediction.points_outcome = POINT_SYSTEM[self.stage]['outcome']
                else:
                    prediction.points_score = 0
                    # check if outcome matches
                    if   prediction.goals1 > prediction.goals2: # team 1 wins
                        prediction.winner = prediction.team1 
                    elif prediction.goals1 < prediction.goals2: # team 2 wins
                        prediction.winner = prediction.team2 
                    else: prediction.winner = 'tie'
                    
                    if prediction.winner == official_winner: 
                        prediction.points_outcome = POINT_SYSTEM[self.stage]['outcome']
                    else: prediction.points_outcome = 0
            else:
                prediction.points_score = 0
                prediction.points_outcome = 0
                
                
                    
                
    
class Prediction(db.Model):
    pred_id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, index=True)
    team1 = db.Column(db.String(3))
    team2 = db.Column(db.String(3))
    goals1 = db.Column(db.Integer)
    goals2 = db.Column(db.Integer)
    winner = db.Column(db.String(64))
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
    goleador_points = db.Column(db.Integer)
    
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
    teams = db.relationship('Team', backref = 'stage', lazy = 'dynamic', cascade="all,delete, delete-orphan")
    
    def get_prediction_results(self, user_id, save_results = True):
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
        
        # determine group winner and runner-up
        top_2_teams = self.teams.order_by(Team.points.desc(), Team.goal_difference.desc(), Team.goals_scored.desc()).all()[:2]
        self.winner, self.runner_up = [t.country_code for t in top_2_teams]
        print(f'{self.name} Top 2: {self.winner}, {self.runner_up}')
        
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
    
class EventTracker(UserMixin, db.Model):
    event_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    description = db.Column(db.String(1024))
    count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(timezone = True), index = True)
    
class Points(UserMixin, db.Model):
    point_id = db.Column(db.Integer, primary_key = True)
    event_description = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    points = db.Column(db.Integer)
    prediction_points = db.Column(db.Integer)
    stage_points = db.Column(db.Integer)
    goleador_points = db.Column(db.Integer)
    
    
    def get_ranking(self):
        ordered_point_obs = Points.query.order_by(Points.points.desc()).all()
        # get current rankings
        position = 1
        current = ordered_point_obs[0].points
        rankings = []
        for p in ordered_point_obs:
            if p.points == current: rankings.append(position)
            else:
                current = p.points
                position += 1
                rankings.append(position)
        ordered_points = [p.points for p in ordered_point_obs]
        ranking = rankings[ordered_points.index(self.points)]
        return ranking

class OfficialStage(db.Model):
    stage_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tournament = db.Column(db.String(64), default = "Qatar 2022")
    stage_type = db.Column(db.String(32))
    name = db.Column(db.String(32)) # A, B, C...
    winner = db.Column(db.String(32))
    runner_up = db.Column(db.String(32))
    team1 = db.Column(db.String(32))
    team2 = db.Column(db.String(32))
    team3 = db.Column(db.String(32))
    team4 = db.Column(db.String(32))

    
    

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

POINT_SYSTEM = {
    'group'     : {'match_score':  5, 'outcome': 10},
    'rd16'      : {'match_score': 25, 'outcome': 50},
    'quarters'  : {'match_score': 30, 'outcome': 60},
    'semis'     : {'match_score': 35, 'outcome': 70},
    'third'     : {'match_score': 40, 'outcome': 80},
    'final'     : {'match_score': 50, 'outcome': 100}
 }