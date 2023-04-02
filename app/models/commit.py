from app import db


class Commit(db.Model):
    __tablename__ = 'commits'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)
    repository_id = db.Column(db.Integer, db.ForeignKey("repositories.id"), index=True, nullable= False)
    repository = db.relationship("Repository",
                                 back_populates="commits",
                                 foreign_keys=[repository_id],
                                 )
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), index=True, nullable=False)
    author = db.relationship("Author",
                                 back_populates="commits",
                                 foreign_keys=[author_id],
                                 )
    test_cases = db.relationship("TestCase")

    def __repr__(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'message': self.message,
            'datetime': self.datetime,
            'repository_id': self.repository_id,
        }

    def to_json(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'message': self.message,
            'datetime': self.datetime,
            'repository_id': self.repository_id,
        }