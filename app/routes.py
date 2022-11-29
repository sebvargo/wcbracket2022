from app import app, db
from flask import render_template, redirect, flash, url_for, request, session
from app.models import User, Prediction, Goleador, Stage, EventTracker, Game, Points
from app.utility_functions import FLAGS, read_group_stage_bracket, read_goleador, calculate_group_results, add_event, get_next_games, get_rankings, second_round_games, add_round_two_game
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, QuinielaForm, MoroccoForm, OfficialScoreForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import pandas as pd
import datetime as dt


@app.route('/round2', methods = ['GET', 'POST'])
@login_required
def round2():  

    if request.method == 'POST': 
        for stage, game_ids in second_round_games.items():
            msg, msg_type = add_round_two_game(game_ids, stage, request.form, current_user.user_id)
            flash(msg, msg_type)

    # check if predictions are already in DB
    if Prediction.query.filter_by(user_id = current_user.user_id, stage = "rd16").first() is not None:
        load_data = True
        games = {}
        games['rd16'] = Prediction.query.filter_by(user_id = current_user.user_id, stage = "rd16").order_by(Prediction.game_id).all()
        games['quarters'] = Prediction.query.filter_by(user_id = current_user.user_id, stage = "quarters").order_by(Prediction.game_id).all()
        games['semis'] = Prediction.query.filter_by(user_id = current_user.user_id, stage = "semis").order_by(Prediction.game_id).all()
        games['third'] = Prediction.query.filter_by(user_id = current_user.user_id, stage = "third").order_by(Prediction.game_id).first()
        games['final'] = Prediction.query.filter_by(user_id = current_user.user_id, stage = "final").order_by(Prediction.game_id).first()
        games['finals'] =  [games['final'], games['third']]
        
    else:
        load_data = False
        games = {
        'rd16': Game.query.filter(Game.stage == 'rd16').order_by(Game.game_id).all(),
        'quarters': Game.query.filter(Game.stage == 'quarters').order_by(Game.game_id).all(),
        'semis': Game.query.filter(Game.stage == 'semis').order_by(Game.game_id).all(),
        'finals': Game.query.filter(Game.game_id > 62).order_by(Game.game_id.desc()).all()
    }
    return render_template('round2.html', title='Round 2', user = current_user, load_data = load_data, games = games, flags = FLAGS)

@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():    
    ranking = current_user.points.first().get_ranking()
    official_games = Game.query.order_by(Game.game_id).all()
    predictions = Prediction.query.filter_by(user_id = current_user.user_id, stage = 'group').order_by(Prediction.game_id).all()
    group_stage_predictions = zip(predictions, official_games)
    goleador = Goleador.query.filter_by(user_id = current_user.user_id).first()
    stage_results = current_user.stages.order_by(Stage.name).all()
    return render_template('index.html', title='Mis Predicciones', group_stage_predictions = group_stage_predictions, ranking = ranking, goleador = goleador, stage_results = stage_results, flags = FLAGS)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        add_event(description = 'login', user = current_user, init_value = 1)
        session['user_id'] = user.user_id
        return redirect(url_for('results'))    
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page) 
    return render_template('login.html', title = 'Login', form = form, hide_links = True)

@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    form = QuinielaForm()
    if form.validate_on_submit():
        f = form.file.data
        read_group_stage_bracket(f)
        read_goleador(f)
        calculate_group_results(current_user, stage_type = 'group')
        return redirect(url_for('index'))
    add_event("view_results", current_user)
    return render_template('upload.html', title = 'Upload Quiniela', form = form)

@app.route('/logout')
def logout():
    logout_user()
    session['user_id'] = None
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username} Welcome/Bienvenido!', 'info')
        return redirect(url_for('login'))
    
    return render_template('register.html', title = 'register', form = form)

@app.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        try:
            game_id = request.form['btn_submit'] 
            goals1 = request.form.get("goals1")
            goals2 = request.form.get("goals2")
            if goals1 is None or goals2 is None: 
                flash('Please add scores', 'danger')
                return
            game_to_edit = Game.query.filter_by(game_id = game_id).first()
            game_to_edit.official_goals1 = goals1
            game_to_edit.official_goals2 = goals2
            game_to_edit.calculate_user_points()
            # compare official result to predictions
            description = f'Game {game_id} | {game_to_edit.team1} {goals1} - {goals2} {game_to_edit.team2}'
            try:
                db.session.commit()
                print(f'{description} update was successful')
                flash(f'{description} update was successful', 'success')
            except:
                db.session.rollback()
                print(f'{description} update was NOT successful')
                flash(f'{description} update was NOT successful', 'danger')
                return
        
        except Exception:
            flash(Exception, 'danger')
        
        # Calculate points
        game_to_edit.calculate_user_points()
        try:
            db.session.commit()
            print(f'{description} update was successful')
            flash(f'{description} update was successful', 'success')
        except:
            db.session.rollback()
            print(f'{description} update was NOT successful')
            flash(f'{description} update was NOT successful', 'danger')
            return
        
    points = Points.query.order_by(Points.points.desc()).all()
    games = get_next_games(days_back = 0, days_ahead = 0)
    add_event("view_admin", current_user)
    return render_template('admin.html', 
                           title = 'admin',
                           points = points, zip = zip, games = games, dt = dt, flags = FLAGS)

@app.route('/calculate_points', methods = ['GET', 'POST'])
@login_required
def calculate_points():
    users = User.query.all()
    check = []
    for user in users: 
        calc = user.calculate_points(event_description = '2022_quiniela_qatar')
        check.append(calc)
    flash(f'{sum(check)}/{len(check)} points calculated succesfully', 'success')
    return redirect(url_for('admin'))

@app.route('/calendar', methods = ['GET'])  
@login_required 
def calendar():
    games = Game.query.order_by(Game.local_time).all()
    add_event("view_calendar", current_user)
    return render_template('calendar.html', title = 'Calendario Qatar 2022', games = games, flags = FLAGS, dt = dt)

@app.route('/results', methods = ['GET'])  
@login_required
def results():
    current_user_rank = current_user.points.first().get_ranking()
    ordered_point_obs = Points.query.order_by(Points.points.desc()).all()
    rankings, points = get_rankings(ordered_point_obs=ordered_point_obs)
    rankings_and_points = zip(rankings, ordered_point_obs)
    games = get_next_games(days_back =0, days_ahead = 0)
    avg_goals = []
    for g in games:
        avg_goals.append(g.get_average_goal_prediction())
    games = zip(games, avg_goals)
    add_event("view_results", current_user)
    return render_template('results.html', title = 'Resultados/Results', rankings_and_points = rankings_and_points, current_user_rank = current_user_rank, flags = FLAGS, games = games, dt = dt)

@app.route('/user_profile/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def user_profile(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    ranking = user.points.first().get_ranking()
    points = Points.query.filter_by(user_id = user_id).first().points
    stage_results = user.stages.order_by(Stage.name).all()
    goleador = user.goleador.first()
    
    official_games = Game.query.order_by(Game.game_id).all()
    predictions = Prediction.query.filter_by(user_id = user.user_id, stage = 'group').order_by(Prediction.game_id).all()
    group_stage_predictions = zip(predictions, official_games)
    add_event("view_results", current_user)
    return render_template('user_profile.html', title = f'Profile: {user.username}', ranking = ranking, user = user, group_stage_predictions = group_stage_predictions, flags = FLAGS,
                            stage_results = stage_results, goleador = goleador, points = points)
    
@app.route('/rollback', methods = ['GET', 'POST'])
@login_required
def rollback():
    db.session.rollback()
    flash('Rollback Session Succesful', 'info')
    return redirect(url_for('admin'))

@app.route('/predictions/<int:game_id>', methods = ['GET', 'POST'])
@login_required
def predictions(game_id):
    game = Game.query.filter_by(game_id = game_id).first()
    avg_goals_tuple = game.get_average_goal_prediction()
    predictions = Prediction.query.filter_by(game_id = game_id)
    official = [game.official_goals1, game.official_goals2]
    return render_template('all_user_predictions.html', title = 'Posiciones/Rankings', official = official, game = game, avg_goals_tuple = avg_goals_tuple, flags = FLAGS, predictions = predictions, dt = dt)

@app.route('/api/user_events', methods = ['GET'])
@login_required
def get_user_events():
    d={}
    for u, e in db.session.query(User, EventTracker).filter(User.user_id == EventTracker.user_id).order_by(User.username).all():
        if u.username not in d.keys():
            d[u.username] = {}
        d[u.username][e.description] = e.count
    return d


@app.route('/api/event_count', methods = ['GET'])
@login_required
def event_count():
    d={}
    for u, e in db.session.query(User, EventTracker).filter(User.user_id == EventTracker.user_id).order_by(User.username, EventTracker.description).all():
        if e.description not in d.keys():
            d[e.description] = {}
        d[e.description][u.username] = e.count

    for e in d.keys():
        d[e] = {k: v for k, v in sorted(d[e].items(), key=lambda item: item[1], reverse=True)}
    
    return d