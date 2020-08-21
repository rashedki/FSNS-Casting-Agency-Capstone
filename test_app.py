import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *

executive_producer_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1EZEdNMFpCTURFeU16WkZNems0UWtFMFJUZzNRak16UkVFMlJqQXdNVVpCT1RKQk5EYzROUSJ9.eyJpc3MiOiJodHRwczovL2lmYXRpbWFoLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTI4ZWI0MGY4ZjU1YTBlYWFhOTVmZjkiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4MDUyNjg0OCwiZXhwIjoxNTgzMTE4ODQ4LCJhenAiOiJmanlKaFd3MDZBTVdUN3MzWnp0cU1GMzhkc0g5dU94cyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSJdfQ.ZDOj8k8nZ0NdmrS-6xU3rBSEAPmqtedHIxI_u4B6Z7TwrisH68lCm_poE3BbSCjtgc0-26g2yxYjXwJBbj1eYGkGfvFxw9W4Aab4L0U3odp3VVBoh8QCHaeXxvXx0aK1sltoZLV-U14STVhd2kaEMigMeeVW1W7set7dFb17KwMfh2yt68ukUusGUCMh34upD2E0-sjFRerXDIjXJfNnrDGS5L4g6BbfTSAwy_dSuajZQaGuCYQU-DKBo0SUhUebAXQTqoUSf2wctq6ttQdRbtYAkCw5E8xgLmtpo_LiJpBkVbluy94qfASQlIUjTcrizAy44btgbfJVYIGiuYOIgQ'}
casting_director_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1EZEdNMFpCTURFeU16WkZNems0UWtFMFJUZzNRak16UkVFMlJqQXdNVVpCT1RKQk5EYzROUSJ9.eyJpc3MiOiJodHRwczovL2lmYXRpbWFoLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTI5MDExZjJmNWNjODBlOTg2Y2ZkOTUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4MDUzMTUxOSwiZXhwIjoxNTgzMTIzNTE5LCJhenAiOiJmanlKaFd3MDZBTVdUN3MzWnp0cU1GMzhkc0g5dU94cyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9yIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIl19.krU8wi3-DOgVeAzPX4jXqsbXTE4XbEc3T5t67nzE56bF3DCJVFLA5nqDxPHCO1iQ6Vph_CWFvsb9WFXhfWIjYhyCq4e4XKuhtNTr3eQwYycweZsWdcQgTnx9PGRwNRUNHi3DKLBYD1M85zmYDpeDzIjjluXKNxLZ855dtQRv22YWkKHuWpQ6Islxdggs_qbbHnV1ojOGYnm5DZDHWhMBV3SPiYqxBJhI1E8PGNf_lNmOqzMOqzzvmvaZIDMLoVkIacruqs72Mo49X0RStNBFAGBboUSQT8mcVlQB0AQywpLvpZYw-LqsgMmKnonA4PhxFsM5sEOL1KsSd-8UydEHsw'}
casting_assistant_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1EZEdNMFpCTURFeU16WkZNems0UWtFMFJUZzNRak16UkVFMlJqQXdNVVpCT1RKQk5EYzROUSJ9.eyJpc3MiOiJodHRwczovL2lmYXRpbWFoLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTM0YzRiM2FhYTFmMDBlNjU1NDkyZjQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4MDUzMTU3MCwiZXhwIjoxNTgzMTIzNTcwLCJhenAiOiJmanlKaFd3MDZBTVdUN3MzWnp0cU1GMzhkc0g5dU94cyIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.eV8f45n2BNon5n7DgtdcUvvlEYguLyhLER7pdNwQi_A_oUogyGEcVTtoMMaJMNYAIInRfD8ovqJ91O33-BfQco6M23FhnydhJkz7xsrEJxB1XuX-fpIhglF1LPh5eTDnRJyTiKH6nmEFBPpDJVYrL5BY-T9LsNZe_2TluczlKh3boDIh0ShV2ekvdJFdQjJxgWVd8_LhOCXS1h8GuIY6LwCLx1vHJN7KZXuUVDTgSz82t_SbH6qOkD7ZKUFFNIlDAPKisYQtjaRUBH-IyMgWTu9PGV-6A-82vTtyy96JN_dt1i3FKKlheYc4dXepH1Odib5ATHCDybqgWd0rzoJU-A'}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(None)
        self.client = self.app.test_client
        self.database_name = "capstone_database_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'khalil', 'localhost:5432', self.database_name)
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
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    # -------------------------------------------------------------------------
    # GET Endpoint Tests
    # Creating a test for the movies GET endpoint
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_not_allowed(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Creating a test for the acotrs GET endpoint
    def test_get_actors(self):
        # Retrieving information from endpoint
        res = self.client().get('/actors')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_not_allowed(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # POST Endpoint Tests
    # -------------------------------------------------------------------------

    # Creating a test for the /movies/create POST endpoint
    def test_post_movie(self):
        # Posting dummy movie data to movies POST endpoint
        res = self.client().post('/movies/2', json = self.test_movie)
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    # Creating a test for the /actors/create POST endpoint
    def test_post_actor(self):
        # Posting dummy actor data to movies POST endpoint
        res = self.client().post('/actors/2', json = self.test_actor)
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    def test_404_sent_requestiong_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm": "k"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_not_exist_question_(self):
        res = self.client().post('/questions/search',
                                 json={"searchTerm": "axasdad"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertFalse(len(data['questions']))

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_get_question_by_not_exist_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quizzes(self):
        res = self.client().post('/quizzes',
        json={"previous_questions": [],
               "quiz_category": {"type": "Science",
               "id": 1
              }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_422_no_data_given_quizzes(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
