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

After installing the dependencies, execute the bash file setup.sh to set the user jwts, auth0 credentials and the remote database url by naviging to the root directory of this project and running (Note: for now I just added the DATABASE_URL link:
```sh
source setup.sh
```

##### Running the server

From within the root directory first ensure you are working using your virtual environment.

To run the server, execute:
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

###### GET /movies

Gets all movies from the db.


###### POST /movies

Adds a new movie to the db.


###### PATCH /movies/<int:movie_id>

Edit data on a movie in the db.


###### DELETE /movies/<int:movie_id>

Delete a movie from the db.


###### GET /actors

Gets all actors from the db.


###### POST /actors

Adds a new actor to the db.


###### PATCH /actors/<int:actor_id>

Edit data on a actor in the db.


###### DELETE /actors/<int:actor_id>

Delete a actor from the db.


### Tests

To run the tests, run the follwoing script in your terminal:
```sh
python3 test_app.py
```
