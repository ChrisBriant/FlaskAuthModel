from app.extensions import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(75))
    email = db.Column(db.String(100), unique=True)
    is_enabled = db.Column(db.Boolean())

    def __repr__(self):
        return f'<Account "{self.username}">'