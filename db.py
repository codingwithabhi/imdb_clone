import ast
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserDetails(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, index=True)
    password = db.Column(db.String)
    token = db.Column(db.String)
    user_type = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'token': self.token,
            'created_on': str(self.created_on) if self.created_on else None,
            'updated_on': str(self.updated_on) if self.updated_on else None
        }


class MovieDetails(db.Model):
    __tablename__ = 'movie_details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    popularity = db.Column(db.String)
    director = db.Column(db.String)
    imdb_score = db.Column(db.String)
    genre = db.Column(db.String)
    added_by = db.Column(db.String)
    edited_by = db.Column(db.String)

    def to_json(self):
        return {
            'name': self.name,
            'popularity': self.popularity,
            'director': self.director,
            'imdb_score': self.imdb_score,
            'genre': ast.literal_eval(self.genre) if self.genre else None,
        }



