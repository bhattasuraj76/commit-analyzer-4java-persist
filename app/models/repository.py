from app import db


class Repository(db.Model):
    __tablename__ = 'repositories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    commits = db.relationship("Commit",
                                 order_by="Commit.datetime",
                                 passive_deletes=True
                                 )

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
        }

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
        }