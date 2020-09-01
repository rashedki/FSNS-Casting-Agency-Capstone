from os import environ
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *
from auth import AuthError, requires_auth
from sqlalchemy import func, desc

executive_token = os.environ.get('CASTING_EXECUTIVE_PRODUCER_TOKEN')
casting_executive_producer = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + executive_token}
director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
casting_director = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + director_token}
assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_assistant = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + assistant_token}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(None)
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".\
            format('khalil', '', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'New Movie Title 1',
            'release_date': '01-09-2020'
        }

        self.new_movie_2 = {
            'title': 'New Movie Title 2',
            'release_date': '02-09-2020'
        }

        self.update_movie = {
            'title': 'Toy Story 12',
            'release_date': '03-09-2022'
        }

        self.new_actor = {
            'name': 'New Actor Name 1',
            'age': 20,
            'gender': 'M',
            'movie_id': '1'
        }

        self.new_actor_2 = {
            'name': 'New Actor Name 2',
            'age': 30,
            'gender': 'F',
            'movie_id': '2'
        }

        self.update_actor = {
            'name': 'Khalil',
            'age': 40,
            'gender': 'M',
            'movie_id': '2'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # drop all tables
            self.db.drop_all()
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(str(data['movies'])))

    def test_get_movies_not_authorized(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movie_details(self):
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().get(f'/movies/{movie.id}',
                                     headers=casting_assistant)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movie', data)
        # movies length should be more than 0
        self.assertGreater(len(str(data['movie'])), 0)

    def test_get_invalid_movie(self):
        '''
        tests getting movies by invalid id
        '''
        # get the last movie from db
        movie = Movie.query.order_by(desc(Movie.id)).first()
        # get response json, then load the data
        response = self.client().get(f'/movies/{movie.id + 1}',
                                     headers=casting_assistant)
        data = json.loads(response.data)
        # status code should be 404
        self.assertEqual(response.status_code, 404)
        # success should be false
        self.assertFalse(data['success'])

    # Creating a test for the acotrs GET endpoint
    def test_get_all_actors(self):
        # Retrieving information from endpoint
        res = self.client().get('/actors', headers=casting_assistant)
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_not_allowed(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actor_details(self):
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().get(f'/actors/{actor.id}',
                                     headers=casting_assistant)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actor', data)
        # actors length should be more than 0
        self.assertGreater(len(str(data['actor'])), 0)

    def test_get_invalid_actor(self):
        '''
        tests getting actors by invalid id
        '''
        # get the last actor from db
        actor = Actor.query.order_by(desc(Actor.id)).first()
        # get response json, then load the data
        response = self.client().get(
            f'/actors/{actor.id + 1}', headers=casting_assistant)
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])

    # POST Endpoint Tests
    # ---------------------------------------------
    # Creating a test for the /movies/create POST endpoint
    def test_post_movie(self):
        # Posting dummy movie data to movies POST endpoint
        res = self.client().post('/movies', headers=casting_executive_producer,
                                 json={'title': 'test posting new movie2',
                                       'release_date': '01-10-2021',
                                       })
        # Transforming body response into JSON
        data = json.loads(res.data)
        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        # movies should be present in data
        self.assertIn('movies', data)

    def test_empty_post_movie(self):
        '''
        tests posting an empty movie json
        '''
        # get response json, then load the data
        response = self.client().post('/movies',
                                      headers=casting_executive_producer,
                                      json={})
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_post_movie(self):
        '''
        tests posting new movie with a role below the minimum role
        '''
        # get response json, then load the data
        response = self.client().post(
            '/movies',
            headers=casting_director,
            json={
                'title': 'test movie from unuathorized',
                'release_date': '01-01-2022'
            })
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    # Creating a test for the /actors/create POST endpoint
    def test_post_actor(self):
        '''
        tests posting a new actor
        '''
        # get response json, then load the data
        response = self.client().post(
            '/actors',
            headers=casting_director,
            json={
                'name': 'test posting artist from authorized',
                'age': '42',
                'gender': 'M',
                'movie_id': 4
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(str(data['actors'])), 0)

    def test_empty_post_actor(self):
        '''
        tests posting an empty actor json
        '''
        # get response json, then load the data
        response = self.client().post('/actors',
                                      headers=casting_director,
                                      json={})
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_post_actor(self):
        '''
        tests posting new actor with a role below the minimum role
        '''
        # get response json, then load the data
        response = self.client().post(
            '/actors',
            headers=casting_assistant,
            json={
                'name': 'test artist from unauthorized',
                'age': '42',
                'gender': 'M',
                'movie_id': 5
            })
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    # PATCH (Update) Endpoint Tests
    # -------------------------------------------------------------------------
    # Creating a test to update a movie with new info
    def test_patch_movie(self):
        '''
        tests patching a movie
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().patch(
            f'/movies/{movie.id}',
            headers=casting_director,
            json={
                'title': 'updated movie name2'
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(str(data['movies'])), 0)

    def test_unauthorised_patch_movie(self):
        '''
        tests patching new movie with a role below the minimum role
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().patch(
            f'/movies/{movie.id}', headers=casting_assistant,
            json={
                'title': 'updated movie'
            })
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_empty_patch_movie(self):
        '''
        tests patching a movie with empty json
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().patch(
            f'/movies/{movie.id}',
            headers=casting_director,
            json={}
            )
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])

    def test_patch_actor(self):
        '''
        tests patching an actor
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().patch(
            f'/actors/{actor.id}',
            headers=casting_director,
            json={
                'name': 'updated actor name'
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(str(data['actors'])), 0)

    def test_unauthorised_patch_actor(self):
        '''
        tests patching new actor with a role below the minimum role
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().patch(
            f'/actors/{actor.id}',
            headers=casting_assistant,
            json={
                'name': 'updated actor'
            })
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_empty_patch_actor(self):
        '''
        tests patching an actor with empty json
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().patch(
            f'/actors/{actor.id}',
            headers=casting_director,
            json={}
            )
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])

    # DELETE Endpoint Tests
    # --------------------------------------------------
    # Creating a test to delete a movie using the DELETE endpoint

    def test_delete_movie(self):
        '''
        tests deleting a movie
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().delete(
            f'/movies/{movie.id}',
            headers=casting_executive_producer
            )
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # delete should be present in data
        self.assertIn('deleted', data)

    def test_unauthorised_delete_movie(self):
        '''
        tests deleting a movie with a role.
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically,
        # then load the data
        response = self.client().delete(
            f'/movies/{movie.id}', headers=casting_director)
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        '''
        tests deleting an actor
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().delete(
            f'/actors/{actor.id}', headers=casting_executive_producer)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # delete should be present in data
        self.assertIn('deleted', data)

    def test_unauthorised_delete_actor(self):
        '''
        tests deleting an actor with a role.
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically,
        # then load the data
        response = self.client().delete(
            f'/actors/{actor.id}', headers=casting_assistant)
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
