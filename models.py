import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_path = "postgresql://khalil@localhost:5432/fsndcapstone"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to
    have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

# Creating a Movies class object to hold / update information about movies
class Movie(db.Model):
    # Setting the name of the table
    __tablename__ = 'movies'

    # Setting attributes of the table
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)

    # Connecting actors from the 'actors' table to the respective movie
    actors = db.relationship('Actor', backref = 'movies')

    # Creating an insert function
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Creating an update function
    def update(self):
        db.session.commit()

    # Creating a delete function
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Creating a formatting function
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

# Creating an Actor class object to hold / update information about actors & actresses
class Actor(db.Model):
    # Setting the name of the table
    __tablename__ = 'actors'

    # Setting the attributes of the table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    # Connecting movie to the respective actors from the movies table
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)
    
    # # To access the actor list of movies
    # movies = db.relationship('Movie', backref = 'actors')
    
    # Creating an insert function
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Creating an update function
    def update(self):
        db.session.commit()

    # Creating a delete function
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Creating a formatting function
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
