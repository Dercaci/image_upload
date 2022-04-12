# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from base import app


db = SQLAlchemy(app)
# migrate = Migrate(app, db)

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    big_image = db.Column(db.String(64), unique = True)
    small_image = db.Column(db.String(64), unique = True)
    