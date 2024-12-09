from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    numbers = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "numbers": self.numbers,
        }