import pandas as pd
from app import db
from app.models import User, Prediction, Goleador
from flask_login import current_user

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
    
