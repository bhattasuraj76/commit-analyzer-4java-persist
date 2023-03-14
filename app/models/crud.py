from app import app, db
from flask_migrate import Migrate
from .repository import Repository
from .test_case import TestCase

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
