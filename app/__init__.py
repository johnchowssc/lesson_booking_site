from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config) # Used to import 'SECRET_KEY' from config file for CSRF.
login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

admin = Admin(app, name='Sydney Sabre', template_mode='bootstrap3')

from app import routes, models

# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin

admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Slot, db.session))