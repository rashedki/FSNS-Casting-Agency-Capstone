import os
from os import environ
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *
from auth import AuthError, requires_auth
from sqlalchemy import func, desc

casting_executive_producer = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJqeXJtZEpnQ0VDTTBLTWp4d2o3MiJ9.eyJpc3MiOiJodHRwczovL3Jhc2hlZGtpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQzOTI5ZGIyMzAzMDAwNjcwNTQxZjYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODQ1OTg5MiwiZXhwIjoxNTk4NDY3MDkyLCJhenAiOiI0R2dWanFnU2prNXo1YkZqR2tMeVRTMmhZUmQwV2hCRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3ItZGV0YWlscyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWUtZGV0YWlscyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.WlyooOMq1DCftlfiJgZqKnvp6F7NHFtpo_rilYV9OcJAahjNX2WKb1J_s58br5E0g1TZoGdbqfr0bBCSHKOd5_BocIAok_sw0fekpADjd7q9R6d1adG9sVwA8v6yTB4sBrBmFhoG9brQf1AQwGNaFBDSSbM6S7LwhTY1InoGljxvd7fRwXQq_4-QIfACPP-zGLXxaqq0ZJ2IKajHyDazkqArWiBkoHrLmIRLzoZAHQ846dFqsQI8hYJJTEEaNNYaj_Xdtm9VS9VlQW2qugdnry73LRh1QvOCVHUhTect24tbBg3-j9xOHHUvM7iI7dEVnUVYBZmCrCNB0m0VZ8YDNg'}
casting_director = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJqeXJtZEpnQ0VDTTBLTWp4d2o3MiJ9.eyJpc3MiOiJodHRwczovL3Jhc2hlZGtpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQzYTQ1ZDhmMThhYTAwNjg5ZTFlYmYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODQ1OTgwMSwiZXhwIjoxNTk4NDY3MDAxLCJhenAiOiI0R2dWanFnU2prNXo1YkZqR2tMeVRTMmhZUmQwV2hCRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3Rvci1kZXRhaWxzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZS1kZXRhaWxzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.AnU5pSzD24DAJVnupPYR58Gf_1-TCgL20it55LWozJxWFII85qR27uF4BtKhDGFFkX0FTSkQgWOjTrNSuMmQhjMxpgBEElXmZyG1cVImSHQpHT-aN1JRo-4H3h72R4WcfM-PPM1DY6UlMbN2cJx6s5ilc-QTI_2kU2gDiP-7gfFNQX6FniWgRucnKwWYhyPEigUUkvTjrczZ7NAb7BaMIAsWYtWweA8qNzST8cwy3FBAruqBhKt_jz7tCNdPCM2fDTolRRrEyTWCTr-aiGoMYrYw6HrhqVfmTWXTpWnvIxqdnQx9hA3ZXgyCEuR9YbEtvvVQ0C24XtUIVC8SkCmyWQ'}
casting_assistant = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJqeXJtZEpnQ0VDTTBLTWp4d2o3MiJ9.eyJpc3MiOiJodHRwczovL3Jhc2hlZGtpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyMzMyN2ExYjQxZjAwNjc4MjE3ZDEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODQ1OTY4MywiZXhwIjoxNTk4NDY2ODgzLCJhenAiOiI0R2dWanFnU2prNXo1YkZqR2tMeVRTMmhZUmQwV2hCRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yLWRldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllLWRldGFpbHMiLCJnZXQ6bW92aWVzIl19.ove7ePDOFcCyMeR6Pn-zQiY8g3FEt-hut74hc118YD22Bczl6arWvWzAYTaDs76WMOH9KE1wspmFvjxwvmq8wl1PpRcWNT35T-S-kTnEfmObv16MPQkLpO1__7UO_YmhqR_D4WwJeLVgtTYR112bhg-hIrSVgojdQ1eOMIeRODCZxgP0gYT0DVqSM7XbrKmZZYyvfve78NM3YWCahv8f2fvT4OqG2NGl6L5RJlAGhr-YLU_Jra5vo-lI5fx2tt_cTAy2Rvhav_ZVK8bg_hfiS54Do3ThKtpt3av-mGcROyO7qtjtRLfyPn8mKkLBC0vdsSHqvyUV5TOgARP_m_xc9A'}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(None)
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('khalil','', 'localhost:5432', self.database_name)
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

            # movie1 = Movie(
            #     title='The Testing Test',
            #     release_date='01-09-2020'
            # )
            # movie1.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    # -------------------------------------------------------------------------
    # GET Endpoint Tests
    # Creating a test for the movies GET endpoint
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
        # get response json, requesting the movie dynamically, then load the data
        response = self.client().get(f'/movies/{movie.id}', headers=casting_assistant)
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
        response = self.client().get(f'/movies/{movie.id + 1}', headers=casting_assistant)
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
        # get response json, requesting the actor dynamically, then load the data
        response = self.client().get(f'/actors/{actor.id}', headers=casting_assistant)
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
    # -------------------------------------------------------------------------
    # Creating a test for the /movies/create POST endpoint
    def test_post_movie(self):
        # Posting dummy movie data to movies POST endpoint
        res = self.client().post('/movies', headers=casting_executive_producer,
                                    json={
                                        'title': 'test posting new movie2',
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
        response = self.client().post('/movies',
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
        response = self.client().post('/actors',
                                    headers=casting_director,
                                    json={
                                        'name': 'test posting artist from authorized',
                                        'age': '42',
                                        'gender': 'M',
                                        'movie_id': 5
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
        response = self.client().post('/actors',
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
        # get response json, requesting the movie dynamically, then load the data
        response = self.client().patch(f'/movies/{movie.id}', headers=casting_director, 
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
        # get response json, requesting the movie dynamically, then load the data
        response = self.client().patch(
            f'/movies/{movie.id}', headers=casting_assistant, json={
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
        # get response json, requesting the movie dynamically, then load the data
        response = self.client().patch(f'/movies/{movie.id}', headers=casting_director, json={})
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
        # get response json, requesting the actor dynamically, then load the data
        response = self.client().patch(f'/actors/{actor.id}', headers=casting_director, 
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
        # get response json, requesting the actor dynamically, then load the data
        response = self.client().patch(f'/actors/{actor.id}', headers=casting_assistant, 
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
        # get response json, requesting the actor dynamically, then load the data
        response = self.client().patch(
            f'/actors/{actor.id}', headers=casting_director, json={})
        data = json.loads(response.data)
        # status code should be 422
        self.assertEqual(response.status_code, 422)
        # success should be false
        self.assertFalse(data['success'])


    # DELETE Endpoint Tests
    # -------------------------------------------------------------------------
    # Creating a test to delete a movie using the DELETE endpoint
    def test_delete_movie(self):
        '''
        tests deleting a movie
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client().delete(f'/movies/{movie.id}', headers=casting_executive_producer)
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
        # get response json, requesting the movie dynamically, then load the data
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
        # get response json, requesting the actor dynamically, then load the data
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
        # get response json, requesting the actor dynamically, then load the data
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
