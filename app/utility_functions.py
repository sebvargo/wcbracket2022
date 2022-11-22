import pandas as pd
from app import db
from flask_login import current_user
from app.models import *
from emoji import emojize
import datetime as dt


TEAM_NAMES_EMOJI = {'ARG' : 'Argentina','AUS':'Australia','BEL':'Belgium','BRA':'Brazil','CMR':'Cameroon','CAN':'Canada','CRC':'Costa_Rica','CRO':'Croatia','DEN':'Denmark','ECU':'Ecuador','ENG':'England','FRA':'France','GER':'Germany','GHA':'Ghana','IRN':'Iran','JPN':'Japan','MEX':'Mexico','MAR':'Morocco','NED':'Netherlands','POL':'Poland','POR':'Portugal','QAT':'Qatar','KSA':'Saudi_Arabia','SEN':'Senegal','SRB':'Serbia','KOR':'South_Korea','ESP':'Spain','SUI':'Switzerland','TUN':'Tunisia','URU':'Uruguay','USA':'United_States','WAL':'Wales'}
FLAGS = {k: emojize(f':{t}:') for k, t in TEAM_NAMES_EMOJI.items()}
# FLAGS = {k: f'/flags/{k}.svg' for k, t in TEAM_NAMES_EMOJI.items()}
# OLD_FLAGS = {'ARG':'🇦🇷','AUS':'🇦🇹','BEL':'🇧🇪','BRA':'🇧🇷','CMR':'🇨🇲','CAN':'🇨🇦','CRC':'🇨🇷','CRO':'🇭🇷','DEN':'🇩🇰','ECU':'🇪🇨','ENG':'🏴󠁧󠁢󠁥󠁮󠁧󠁿','FRA':'🇫🇷','GER':'🇩🇪','GHA':'🇬🇭','IRN':'🇮🇷','JPN':'🇯🇵','MEX':'🇲🇽','MAR':'🇲🇦','NED':'🇳🇱','POL':'🇵🇱','POR':'🇵🇹','QAT':'🇶🇦','KSA':'🇸🇦','SEN':'🇸🇳','SRB':'🇷🇸','KOR':'🇰🇷','ESP':'🇪🇸','SUI':'🇨🇭','TUN':'🇹🇳','URU':'🇺🇾','USA':'🇺🇸','WAL':'🏴󠁧󠁢󠁷󠁬󠁳󠁿'}

def add_games_to_db(filename = 'Quiniela Fixed.xlsx'):

    import datetime as dt
    df = pd.read_excel(filename, sheet_name='Resumen')
    df.columns = [
        'game_id', 'date', 'team1', 'team2', 'stage_name', 'local_time', 'location',
        'stage', 'fixture_cell1', 'fixture_cell2', 'team1_prediction', 'team2_prediction']
    times = [dt.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S") for date, time in zip(df['date'].astype(str).values, df['local_time'].astype(str).values)]
    df['datetime'] = times
    df = df.drop(labels = ['fixture_cell1', 'fixture_cell2', 'team1_prediction', 'team2_prediction', 'date', 'local_time'], axis = 1 )
    

    for obj in Game.query.all(): db.session.delete(obj)
    db.session.commit()

    for i in range(df.shape[0]):
            data = df.iloc[i]
            game_id = int(data['game_id'])
            date = data['datetime']
            local_time = data['datetime']
            team1 = data['team1']
            team2 = data['team2']
            stage = data['stage']
            group = str(data['stage_name'])
            location = data['location']
            group = group if group != 'nan' else '-'
            g = Game(
            game_id = game_id,
            local_time = local_time, team1 = team1,team2 = team2,stage = stage,group = group, location=location)
            db.session.add(g)
        
    description = "Add GAMES"    
    try:
        db.session.commit()
        print(f' {description} update was successful')
    except:
        db.session.rollback()
        print(f'{description} update was NOT successful')
    
    
       
def add_event(description, user, init_value = 1):
        if EventTracker.query.filter_by(user_id = user.user_id, description = description).first() is not None:
            event = EventTracker.query.filter_by(user_id = user.user_id, description = description).first()
            event.count += 1
        else:
            event = EventTracker(user_id = user.user_id, description = description, count = init_value)
            db.session.add(event)
        try:
            db.session.commit()
            print(f'{user.username} - {description} update was successful')
        except:
            db.session.rollback()
            print(f'{user.username} - {description} update was NOT successful')
            
def read_group_stage_bracket(xlsx_file, stage = 'group'):
    cols = ['match_id', 'team1', 'team2', 'team1_prediction', 'team2_prediction', 'stage']
    df = pd.read_excel(xlsx_file,sheet_name='Resumen', usecols = cols)
    df = df.loc[df['stage'] == stage]
    
    # check if user has predictions in db, if so delete existing predictions
    if Prediction.query.filter_by(user_id = current_user.user_id, stage = 'group').first() is not None:
        Prediction.query.filter_by(user_id = current_user.user_id, stage = 'group').delete()
    
    print(f'{current_user.user_id}, {current_user.username}')
    # add predictions to database
    for match_id, team1, team2, goals1, goals2, stage in zip(df['match_id'], df['team1'], df['team2'], df['team1_prediction'], df['team2_prediction'], df['stage']):
        g = Prediction(game_id = match_id, team1 = team1, team2 = team2, goals1 = goals1, goals2 = goals2, user_id = current_user.user_id, stage = stage)
        # print(f'Adding: {g.pred_id}')
        db.session.add(g)
    try:
        db.session.commit()
        print(f'Added predictions successfully for {current_user.user_id}-{current_user.username}.')
        return 'Added predictions successfully.'
    
    except:
        db.session.rollback()
        print('Could not add predictions, please try again.')
        return 'Could not add predictions, please try again.'
    
def read_goleador(xlsx_file):
    
    USER_ID = current_user.user_id
    
    df = pd.read_excel(xlsx_file,sheet_name='Goleador - Top Scorer')
    goleador = df['Goleador del mundial  / Top Scorer'].values[0]

    # check if goleador is already in db 
    if Goleador.query.filter_by(user_id = USER_ID).first() is not None:
        Goleador.query.filter_by(user_id = USER_ID).delete()
    # add goleador to db
    g = Goleador(prediction = goleador,user_id = USER_ID)
    db.session.add(g)
    try:
        db.session.commit()
        print(f'Added goleador successfully for {USER_ID}')
        return 'Added predictions successfully.'
    except:
        db.session.rollback()
        print('Could not add goleador, please try again.')
        return 'Could not add predictions, please try again.'
    
    
def create_group_stage(user_id, stage_type):
    # Create all groups for user:
    # check if user already has groups created
    if Stage.query.filter_by(user_id = user_id).first() is not None:
        for stage in Stage.query.filter_by(user_id = user_id, stage_type = stage_type).all():
            # delete any corresponding the stage
            Team.query.filter_by(stage_id = stage.stage_id).delete()
        # delete stage
        Stage.query.filter_by(user_id = user_id).delete()
        
    # create groups
    for group_name in GROUPS.keys():
        stage = Stage(stage_type = stage_type, name = group_name, user_id = user_id)
        db.session.add(stage)

    # add teams to group 
    for group_name in  GROUPS.keys(): # A, B, C ...
        stage_id = Stage.query.filter_by(stage_type =stage_type, name = group_name, user_id = user_id).first().stage_id

        for country_code in GROUPS[group_name]: # QAT, ECU, ...
            team = Team(name = TEAM_NAMES[country_code], country_code = country_code, stage_id = stage_id)
            db.session.add(team)

    try:
        db.session.commit()
        print("Created stages and teams successfully")
    except:
        db.session.rollback()
        print("DID NOT create  stages and team successfully successully. Session rolled back")  

def calculate_group_results(user, stage_type = 'group'):
    print(user.username)
    if len(Stage.query.filter_by(user_id = user.user_id).all()) > 1:
        print(f'{user.username} has Stages')
    else:
        print(f'{user.username} has NO Stages')
        
    # Create stages
    create_group_stage(user.user_id, stage_type)
    
    # get results
    for s in user.stages.all():
        s.get_prediction_results(user.user_id)
        
def get_next_games(days_back =1, days_ahead = 1):
    today = dt.date.today()
    yesterday = dt.date.today() - dt.timedelta(days=days_back)
    tomorrow = dt.date.today() + dt.timedelta(days=days_ahead)
    games = Game.query.filter(Game.local_time >= yesterday, Game.local_time <= tomorrow + dt.timedelta(days=1)).order_by(Game.local_time).all()
    return games
    
def get_rankings(ordered_point_obs):
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
    return rankings, ordered_points