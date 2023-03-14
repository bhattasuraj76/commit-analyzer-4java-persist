from enum import Enum

from app import db


class TestCaseType(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


class TestCase(db.Model):
    __tablename__ = 'test_cases'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=True, unique=True)
    filename = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum(TestCaseType), nullable=False)
    repository_id = db.Column(db.Integer, db.ForeignKey("repositories.id"), index=True)
    repository = db.relationship("Repository",
                                 back_populates="test_cases",
                                 foreign_keys=[repository_id],
                                 )

    # def __repr__(self):
    #     return "<TestCase name={name} url={url}>".format(name=self.name, url=self.url)
