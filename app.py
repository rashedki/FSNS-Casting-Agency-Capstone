import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

#importing objects from other files in this repo.
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor, db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources = {r"/api/": {"origins": "*"}})

  setup_db(app)

  # GET Endpoints
  # Creating an endpoint to view movie information
  @app.route('/movies', methods = ['GET'])
  @requires_auth('get:movies')
  def get_movies():
      # Querying all the movies
      movies = Movie.query.all()

      # Ensuring results are returned otherwise throwing error
      if not movies:
        abort(404)

      # Formatting the returned movie results
      movies = [movie.format() for movie in movies]

      # Formatting the actors field within movies
      for movie in movies:
        movie['actor'] = [actor.format() for actor in movie['actors']]

      return jsonify({
        'success': True,
        'movies': movies
      })

  # Creating an endpoint to view actor information
  @app.route('/actors', methods = ['GET'])
  @requires_auth('get:actors')
  def get_actors():
      # Querying all the actors
      actors = Actor.query.all()

      # Ensuring results are returned else giving error
      if not actors:
        abort(404)

      # Formatting the return actor results
      actors = [actor.format() for actor in actors]

      # Returning actor information
      return jsonify({
          'success': True,
          'actors': actors
      })
  
  # Creating an endpoint to allow a new movie to be added
  @app.route('/movies', methods = ['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
      # Getting information from request body
      body = request.get_json()

      # Extracting information from body.
      movie_title = body.get('title')
      movie_release_date = body.get('release_date')

      # Checking to see if proper info is present
      if None in (title and release_date):
          abort(422)

      try:
          # Adding new movie object with request body info
          movie = Movie(title = movie_title, release_date=datetime.strptime(movie_release_date, '%Y-%m-%d'))
          movie.insert()

          # Returning success information
          return jsonify({
              'success': True,
              'movie_id': movie.id,
              'movies': [movie.format()],
          })
      except:
          abort(422)

  # Creating an endpoint to allow a new actor to be added
  @app.route('/actors', methods = ['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
      # Getting information from request body
      body = request.get_json()

      # Extracting information from the body
      actor_name = body.get('name')
      actor_age = body.get('age')
      actor_gender = body.get('gender')
      actor_movie_id = body.get('movie_id')

      # Checking to see if proper info is present
      if not 'name' in body:
        abort(422)
      # if not ('name' in body and 'age' in body and 'gender' in body and 'movie_id' in body):
      #     abort(422)

      try:
          # Adding new actor object with request body info
          actor = Actor(name = actor_name,
                        age = actor_age,
                        gender = actor_gender,
                        movie_id = actor_movie_id)
          actor.insert()

          # Returning success information
          return jsonify({
              'success': True,
              'actor_id': actor.id,
              'actors': [actor.format()]
          })
      except:
          abort(422)

  # -------------------------------------------------------------------------
  # DELETE Endpoints

  # Creating endpoint to delete a movie by provided movie_id
  @app.route('/movies/<int:movie_id', methods = ['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
      # Querying movie by provided movie_id
      movie = Movie.query.filter(Movie.id == movie_id)
      movie_availability = movie.one_or_none()

      if movie_availability is None:
        abort(404)

      try:
          # Deleting movie from database
          movie.delete()

          # Returning success information
          return jsonify({
              'success': True,
              'deleted': movie_id
          })
      except:
          abort(422)

  # Creating endpoint to delete an actor by provided actor_id
  @app.route('/actors/<int:actor_id', methods = ['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
      # Querying movie by provided movie_id
      actor = Actor.query.filter(Actor.id == actor_id)
      actor_availability = actor.one_or_none()

      if actor_availabilityis None:
        abort(404)

      try:
          # Deleting movie from database
          actor.delete()

          # Returning success information
          return jsonify({
              'success': True,
              'deleted': actor_id
          })
      except:
          abort(422)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)