from flask import Flask
from config import Config
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config) # Used to import 'SECRET_KEY' from config file for CSRF.
login = LoginManager(app)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
db.create_all()

admin = Admin(app, name='Sydney Sabre', template_mode='bootstrap3')

mail = Mail(app)

from app import routes, models

# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin

admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Slot, db.session))