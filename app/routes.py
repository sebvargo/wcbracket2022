from app import app, db
from flask import render_template, redirect, flash, url_for, request, session
from app.models import User, Prediction, Goleador
from app.utility_functions import read_group_stage_bracket, read_goleador
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, QuinielaForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import pandas as pd

@app.route('/')
@login_required
def index():
    user = f'{current_user.username} - id: {current_user.user_id}'
    group_stage_predictions = Prediction.query.filter_by(user_id = current_user.user_id, stage = 'group').all()
    goleador = Goleador.query.filter_by(user_id = current_user.user_id).first()
    return render_template('index.html', group_stage_predictions = group_stage_predictions, user = user, goleador = goleador)


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
        return redirect(url_for('index'))

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