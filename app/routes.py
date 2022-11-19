from app import app, db
from flask import render_template, redirect, flash, url_for, request, session
from app.models import User, Prediction, Goleador, Stage, EventTracker, Game
from app.utility_functions import FLAGS, read_group_stage_bracket, read_goleador, calculate_group_results, add_event
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, QuinielaForm, MoroccoForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import pandas as pd


@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    form = MoroccoForm()
    if form.validate_on_submit():
        game_26 = Prediction.query.filter_by(user_id = current_user.user_id, game_id = 26).first()
        game_26.goals2 = int(form.goals_morocco.data)
        if EventTracker.query.filter_by(user_id = current_user.user_id, description = "MAR goals update").first() is not None:
            update_morocco_event = EventTracker.query.filter_by(user_id = current_user.user_id, description = "MAR goals update").first()
            update_morocco_event.count += 1
        else:
            update_morocco_event = EventTracker(user_id = current_user.user_id, description = "MAR goals update", count = 1)
            db.session.add(update_morocco_event)
        try:
            db.session.commit()
            print(f'{current_user.username} - Morocco update was successful')
        except:
            db.session.rollback()
            print(f'{current_user.username} - Morocco update was NOT successful')
            
    user = f'{current_user.username} - id: {current_user.user_id}'
    group_stage_predictions = Prediction.query.filter_by(user_id = current_user.user_id, stage = 'group').all()
    goleador = Goleador.query.filter_by(user_id = current_user.user_id).first()
    stage_results = current_user.stages.order_by(Stage.name).all()
    game_26 = Prediction.query.filter_by(user_id = current_user.user_id, game_id = 26).first()
    return render_template('index.html', group_stage_predictions = group_stage_predictions, user = user, goleador = goleador, stage_results = stage_results, flags = FLAGS, form = form, game_26 = game_26)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        add_event(description = 'login', user = current_user, init_value = 1)
        session['user_id'] = user.user_id
        return redirect(url_for('index'))    
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
        flash(f'{user.username} welcome to the Quiniela 2022!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title = 'register', form = form)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    users = User.query.all()
    add_event("view_admin", current_user)
    return render_template('admin.html', 
                           title = 'admin',
                           users = users)
 
@app.route('/calendar', methods = ['GET'])   
def calendar():
    games = Game.query.order_by(Game.local_time).all()
    add_event("view_calendar", current_user)
    return render_template('calendar.html', title = 'Calendario Qatar 2022', games = games, flags = FLAGS)

@app.route('/results', methods = ['GET'])   
def results():
    games = Game.query.order_by(Game.local_time).all()
    add_event("view_results", current_user)
    return render_template('results.html', title = 'Posiciones/Rankings', games = games, flags = FLAGS)