from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config) # Used to import 'SECRET_KEY' from config file for CSRF.
login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

from app import routes, models