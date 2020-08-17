import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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
  @requires_auth('view:movies')
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
  @requires_auth('view:actors')
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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)