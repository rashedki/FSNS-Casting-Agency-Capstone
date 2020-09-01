import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from datetime import datetime
# importing objects from other files in this repo.
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor, db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/": {"origins": "*"}})
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE')
        return response

    # Home greeting test
    @app.route('/')
    def get_greeting():
        excited = os.environ.get('EXCITED')
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    @app.route('/logout')
    def logout():
        message = 'You are loged out, Thank you for your visit'
        return message

    # GET Endpoints
    # Creating an endpoint to view movie information
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        # Querying all the movies
        movies = Movie.query.all()
        # Ensuring results are returned otherwise throwing error
        if not movies:
            abort(404)
        # Formatting the returned movie results
        movies = [movie.format() for movie in movies]
        # Formatting the actors field within movies
        return jsonify({
            'success': True,
            'movies': movies
        })

    # Creating endpoint to get a specific movie by provided movie_id
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movie-details')
    def details_movie(jwt, movie_id):
        # Querying movie by provided movie_id
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        else:
            movie = movie.format()
            return jsonify({
                'success': True,
                'movie': movie
            })
        # except Exception:
        #     abort(422)

    # Creating an endpoint to view actor information
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
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

    # Creating endpoint to get a specific actor by provided actor_id
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actor-details')
    def details_actor(jwt, actor_id):
        # Querying movie by provided actor_id
        actor = Actor.query.filter(Actor.id == actor_id)
        actor_availability = actor.one_or_none()
        try:
            if actor_availability is None:
                abort(404)
            # Returning success information
            return jsonify({
                'success': True,
                'actor': actor_id
            })
        except Exception:
            abort(422)

    # Creating an endpoint to allow a new movie to be added
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        # Getting information from request body
        body = request.get_json()
        # Extracting information from body.
        movie_title = body.get('title')
        movie_release_date = body.get('release_date')
        # Checking to see if proper info is present
        if None in (movie_title, movie_release_date):
            abort(422)
        try:
            # Adding new movie object with request body info
            movie = Movie(title=movie_title, release_date=movie_release_date)
            movie.insert()
            # Returning success information
            return jsonify({
                'success': True,
                'movie_id': movie.id,
                'movies': [movie.format()],
            })
        except Exception:
            abort(422)

    # Creating an endpoint to allow a new actor to be added
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        # Getting information from request body
        body = request.get_json()
        # Extracting information from the body
        actor_name = body.get('name')
        actor_age = body.get('age')
        actor_gender = body.get('gender')
        actor_movie_id = body.get('movie_id')
        # Checking to see if proper info is present
        if 'name' not in body:
            abort(422)
        try:
            # Adding new actor object with request body info
            actor = Actor(name=actor_name,
                          age=actor_age,
                          gender=actor_gender,
                          movie_id=actor_movie_id)
            actor.insert()
            # Returning success information
            return jsonify({
                'success': True,
                'actor_id': actor.id,
                'actors': [actor.format()]
                })
        except Exception:
            abort(422)

    # -------------------------------------------------------------------------
    # DELETE Endpoints
    # Creating endpoint to delete a movie by provided movie_id
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)  # abort if id is not found
        else:
            try:
                movie.delete()
                # return movie id that was deleted
                return jsonify({
                    'success': True,
                    'deleted': movie_id
                })
            except Exception:
                abort(422)

    # Creating endpoint to delete an actor by provided actor_id
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        # Querying actor by provided actor_id
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            # Deleting actor from database
            actor.delete()
            # Returning success information
            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except Exception:
            abort(422)

    # -------------------------------------------------------------------------
    # PATCH (Update) Endpoints
    # Creating an endpoint to update information about a specific movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)
            # get json from body
            body = request.get_json()
            # Raise a 400 error if the title or release_date are not strings,
            # or empty
            if 'title' not in body and 'release_date' not in body:
                abort(400)
            # update the title if it's available in the request body
            if 'title' in body:
                if not isinstance(body['title'], str):
                    # title is not a string
                    abort(400)
                # update the movie's title
                movie.title = body['title']
            # update the release_date if it's available in the request body
            if 'release_date' in body:
                # check that the title is a string
                if not isinstance(body['release_date'], str):
                    # release_date is not a string
                    abort(400)
                # update the movie's release_date
                movie.release_date = body['release_date']
            # update the movie in the database
            movie.update()
            return jsonify({
                'success': True,
                'movies': [movie.format()]
            })
            # Raising exception if error updating movie
        except Exception:
            abort(422)
        # Raising exception if movie could not be found
        else:
            abort(404)

    # Creating an endpoint to update actor information with new attribute info
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(jwt, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)
            # get json from body
            body = request.get_json()
            # Raise a 400 error if the name, age, and gender are not strings,
            # or empty
            if 'name' not in body and 'age' not in body and\
                                      'gender' not in body:
                abort(400)
            # update the age if it's available in the request body
            if 'name' in body:
                if not isinstance(body['name'], str):
                    # name is not a string
                    abort(400)
                # update the actor's title
                actor.name = body['name']
            # update the age if it's available in the request body
            if 'age' in body:
                # check that the age is a string
                if not isinstance(body['age'], str):
                    # age is not a string
                    abort(400)
                # update the actor's age
                actor.age = body['age']
            # update the gender if it's available in the request body
            if 'gender' in body:
                # check that the gender is a string
                if not isinstance(body['gender'], str):
                    # gender is not a string
                    abort(400)
                # update the actor's gender
                actor.gender = body['gender']
            # update the actor in the database
            actor.update()
            return jsonify({
                'success': True,
                'actors': [actor.format()]
            })
        # Raising exception if error updating actor
        except Exception:
            abort(422)
        # Raising exception if actor could not be found
        else:
            abort(404)

    # -------------------------------------------------------------------------
    # Error Handling
    '''
        implement error handlers using the @app.errorhandler(error) decorator
    '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return (jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return (jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404)

    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422)

    @app.errorhandler(AuthError)
    def handle_auth_errors(auth_error):
        return (jsonify({
            'success': False,
            'error': auth_error.status_code,
            'message': auth_error.error['description']
        }), auth_error.status_code)

    return app


# Creating the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
