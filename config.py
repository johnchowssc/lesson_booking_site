import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

class Config(object):
    # Run in terminal to generate secret key
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY = os.environ.get('APP_SECRET_KEY') or '3e47059506e85351f118b2d36f8ea1f0efd706f994cd7bd6229ef2b0eee4516e'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')