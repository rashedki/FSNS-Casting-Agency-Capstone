# FSNS Casting Agency Capstone
 The Casting Agency models is a company that is responsible for creating movies and managing and assigning actors to those movies.

 [Hosted on heroku.](https://fsnd-udacity-capstone.herokuapp.com/)

### Motivation
This is my capstone project for the Udacity FSWD nanodegree.

##### Dependencies
All dependencies are listed in the requirements.txt file. They can be installed by running 
```sh
pip3 install -r requirements.txt
```

##### Running the server
After installing the dependencies, execute the bash file (setup.sh) to set the user jwts, auth0 credentials and the remote database url by naviging to the root directory of this project and running
```sh
source setup.sh
```

From within the root directory first ensure you are working using your virtual environment.

Then to run the server, execute:
```sh
FLASK_APP=app.py
FLASK_ENV=development
flask run
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to flaskr directs flask to use the flaskr directory and the __init__.py file to find the application.

### Auth0 Roles, Permissions

Within Auth0, we have established 3 high level roles and have associated different permissions for each role. Each role is progressive in the sense that a "higher" level role inherits all the permissions from a lower level one.

Here are the roles and permissions as defined in Auth0:

##### Casting Assistant: 
This lowest level role only has basic view capabilities. Permissions include...
```sh 
view:movies
view:actors 
```
##### Casting Director: 
As our middle tier role, this role inherits the same permissions from the Casting Assistant role as well as adds some additional permissions. These include...
```sh 
add:movies
add:actors
patch:movies
patch:actors
```
##### Executive Producer: 
Finally, our highest tier role contains all permissions from the roles already defined above as well as gains a few new permissions around deleting resources. These specific permissions are...
```sh 
delete:movies
delele:actors
```
##### Authentication
For the testing purpose, I have created three registered users:
###### Casting Assistant:
```sh
email: castingassistant@test.com
password: Tt@123456
```
###### Cating Director:
```sh
email: castingdirector@test.com
password: Tt@123456
```
###### Casting Executive Producer:
```sh
email: castingexecutive@test.com
password: Tt@123456
```


### Endpoints:

###### GET '/movies'

Gets all movies from db.

Sample response:

```sh
{
    "movies": [
        {
            "id": 1,
            "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
            "title": "test movie title 1"
        },
        {
            "id": 2,
            "release_date": "Thu, 02 Jan 2020 00:00:00 GMT",
            "title": "test movie title 2"
        },
        {
            "id": 3,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "test movie title 3"
        },
        {
            "id": 4,
            "release_date": "Sat, 04 Jan 2020 00:00:00 GMT",
            "title": "test movie title 4"
        }
    ],
    "success": true
}
```


###### POST '/movies'

Adds a new movie to the db.

Sample response:
```sh
{
    "movie_id": 5,
    "movies": [
        {
            "id": 5,
            "release_date": "Tue, 05 Jan 2021 00:00:00 GMT",
            "title": "test posting new movie 5"
        }
    ],
    "success": true
}
```


###### PATCH '/movies/<int:movie_id>'

Edit data on a movie id# 5 in the db.

Sample response:
```sh
{
    "movies": [
        {
            "id": 5,
            "release_date": "Tue, 05 Jan 2021 00:00:00 GMT",
            "title": "updated movie name2"
        }
    ],
    "success": true
}
```


###### DELETE '/movies/<int:movie_id>'

Delete a movie id#=5 from the db.

Sample response:
```sh
{
    "deleted": 5,
    "success": true
}
```


###### GET '/actors'

Gets all actors from db.
```sh
{
    "actors": [
        {
            "age": 10,
            "gender": "M",
            "id": 1,
            "movie_id": 1,
            "name": "khalil"
        },
        {
            "age": 20,
            "gender": "F",
            "id": 2,
            "movie_id": 2,
            "name": "actor2"
        },
        {
            "age": 30,
            "gender": "M",
            "id": 3,
            "movie_id": 3,
            "name": "actor3"
        },
        {
            "age": 40,
            "gender": "F",
            "id": 4,
            "movie_id": 4,
            "name": "actor4"
        }
    ],
    "success": true
}
```


###### POST '/actors'

Adds a new actor to the db.

Sample response:
```sh
{
    "actor_id": 5,
    "actors": [
        {
            "age": 42,
            "gender": "M",
            "id": 5,
            "movie_id": 4,
            "name": "test posting artist from authorized"
        }
    ],
    "success": true
}
```


###### PATCH '/actors/<int:actor_id>'

Edit data on an actor id#=5 in the db.

Sample response:
```sh
{
    "actors": [
        {
            "age": 42,
            "gender": "M",
            "id": 5,
            "movie_id": 4,
            "name": "updated actor name"
        }
    ],
    "success": true
```


###### DELETE '/actors/<int:actor_id>'

Delete a actor id#=5 from the db.

Sample response:
```sh
{
    "deleted": 5,
    "success": true
}
```


### Tests

To run the tests, run the follwoing script in your terminal:
```sh
source setup.sh
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python3 test_app.py
```
