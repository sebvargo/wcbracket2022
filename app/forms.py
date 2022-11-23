from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Label, IntegerField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from app.utility_functions import FLAGS

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use.')
        
class QuinielaForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['xlsx'], '.xlsx files only!')])
    submit = SubmitField('Submit')
    
class MoroccoForm(FlaskForm):
    goals_belgium = StringField(f'{FLAGS["BEL"]} Belgica')
    goals_morocco = StringField(f'{FLAGS["MAR"]} Marruecos', validators=[DataRequired()])
    submit = SubmitField('Save')
    
class OfficialScoreForm(FlaskForm):
    goals1 = StringField(f'Local', validators=[DataRequired()])
    goals2 = StringField(f'Away', validators=[DataRequired()])
    submit = SubmitField('Save')
    
    def __init__(self, labels = None, **kwargs):
        super().__init__(**kwargs)
        if labels is None:
            labels = ["Local", "Away"]
        self['goals1'].label = Label(self['goals1'].id, labels[0])
        self['goals2'].label = Label(self['goals1'].id, labels[1])
    
