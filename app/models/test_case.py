from enum import Enum

from app import db


class TestCaseType(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


class TestCase(db.Model):
    __tablename__ = "test_cases"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    testcase = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(TestCaseType), nullable=False)
    commit_id = db.Column(db.Integer, db.ForeignKey("commits.id"), index=True)
    commit = db.relationship(
        "Commit",
        back_populates="test_cases",
        foreign_keys=[commit_id],
    )

    def __repr__(self):
        return "<TestCase filename={filename} testcase={testcase}>".format(
            filename=self.filename, testcase=self.testcase
        )
