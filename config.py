import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SESSION_PERMANENT =  False
    SESSION_TYPE = 'filesystem'
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    db_instance = os.environ.get('DB_INSTANCE') 
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') \
    #     or 'postgresql://postgres:memes@localhost:5432/quiniela-dev' #or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # if os.environ.get('DATABASE_TYPE') == 'postgres':
    #     SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_user}@localhost/{db_name}?host=/cloudsql/{db_instance}'