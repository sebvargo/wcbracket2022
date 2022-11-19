from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

app = create_app()
Session(app)
login = LoginManager(app)
login.init_app(app)
login.login_message_category = "warning"
login.login_view = 'login'


migrate = Migrate(app, db)
app.app_context().push()

from app import routes, models, errors