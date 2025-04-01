from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    # Relationships
    favourite = db.relationship('Favourite', back_populates='user', lazy=True)
    watchlist = db.relationship('Watchlist', back_populates='user', lazy=True)
    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Favourite(db.Model):
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tmdb_id = db.Column(db.Integer, nullable=False)

    #relationship
    user = db.relationship('User', back_populates='favourite', lazy=True)


class Watchlist(db.Model):
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tmdb_id = db.Column(db.Integer, nullable=False)

    #relationship
    user = db.relationship('User', back_populates='watchlist', lazy=True)
