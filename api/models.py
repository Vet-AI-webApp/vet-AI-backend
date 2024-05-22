from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User(id = {self.id} , name = {self.name}, age = {self.age})"