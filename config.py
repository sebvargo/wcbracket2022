import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SESSION_PERMANENT =  False
    SESSION_TYPE = 'filesystem'
    DATABASE_USER = os.environ["DB_USER"]  # e.g. 'my-database-user'
    DATABASE_PASSWORD = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    DATABASE_NAME = os.environ["DB_NAME"]  # e.g. 'my-database'
    INSTANCE_UNIX_SOCKET = os.environ["INSTANCE_UNIX_SOCKET"]  # e.g. '/cloudsql/project:region:instance'

    try:
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DATABASE_USER}:{DATABASE_PASSWORD}@/{DATABASE_NAME}?unix_sock={INSTANCE_UNIX_SOCKET}/.s.PGSQL.5432'
        # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    except:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        if SQLALCHEMY_DATABASE_URI is None:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
        else:
            SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
