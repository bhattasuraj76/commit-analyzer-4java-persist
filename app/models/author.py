from app import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    commits = db.relationship("Commit",
                                 order_by="Commit.datetime",
                                 )

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }