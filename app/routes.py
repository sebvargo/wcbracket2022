from app import app
from flask import render_template, redirect, flash
from app.forms import LoginForm

@app.route('/')
def index():
    user = {'username': 'seb'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]
    return render_template('index.html', title = 'Home', user = user, posts = posts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember me = {form.remember_me.data}')
        return redirect('/')
    return render_template('login.html', title = 'Login', form = form)