import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SESSION_PERMANENT =  False
    SESSION_TYPE = 'filesystem'
    DB_USER = os.environ.get("DB_USER")  # e.g. 'my-database-user'
    DB_PASS = os.environ.get("DB_PASS")  # e.g. 'my-database-password'
    DB_NAME = os.environ.get("DB_NAME")  # e.g. 'my-database'
    INSTANCE_UNIX_SOCKET = os.environ.get("INSTANCE_UNIX_SOCKET")  # e.g. '/cloudsql/project:region:instance'
    SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{nam}:{pas}@localhost/{dbn}?unix_socket=/cloudsql/{con}').format (
        nam=DB_USER,
        pas=DB_PASS,
        dbn=DB_NAME,
        con=INSTANCE_UNIX_SOCKET,
)
    # try:
    #     SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PASS}@/{DB_NAME}?unix_sock={INSTANCE_UNIX_SOCKET}/.s.PGSQL.5432'
    #     # SQLALCHEMY_DATABASE_URI = os.environn.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    # except:
    #     SQLALCHEMY_DATABASE_URI = os.environn.get('DATABASE_URL')
    #     if SQLALCHEMY_DATABASE_URI is None:
    #         SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    #     else:
    #         SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://')
    #     SQLALCHEMY_TRACK_MODIFICATIONS = False
