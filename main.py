from app import app

if __name__ == "__main__":
    app.run(debug=True)

# import flask

# import os
# import dotenv
# import flask_sqlalchemy
# import datetime

# ## Import forms
# import forms

# ## Initialise environment variables from .env file.
# dotenv.load_dotenv()

# ## Initialise Flask
# app = flask.Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")

## Initialise Bootstrap
# flask_bootstrap.Bootstrap(app)

# ## Initialise DB
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///bookings.db") ## Use Heroku Postgres, or if not found, e.g. local, SQLite
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = flask_sqlalchemy.SQLAlchemy(app)

# ## Configure tables
# class Slot(db.Model):
#     __tablename__ = "slots"
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Date, nullable=False)
#     time = db.Column(db.Time, nullable=False)
#     name = db.Column(db.String(250), nullable=True)

# db.create_all()