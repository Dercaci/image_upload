from flask_migrate import Migrate
from base import app
from models import db, Image


migrate = Migrate(app, db)
