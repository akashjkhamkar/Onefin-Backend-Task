# Onefin Backend Task
### Problem Statement
We need to develop a web application which allows people to create collections of movies they like. There are two parts to this:

---
#### Submission
live - https://onefin-backend-task-akash.herokuapp.com/

---
#### Setup
1. Create a python env
``virtualenv onefinTask_env ``
2. Activate
``source onefinTask_env/bin/activate ``
3. Install dependencies
``pip3 install -r requirements.txt``
4. run
``python3 manage.py runserver``

####  Usage  
1. login at /register , send 'username' and 'password' in a json object
	- logging with a username for a first time will create a new user, next time make sure you 	 use the exact same password 
	- (both sign in and log in activites happen on the /register route)
2. Use the received token to make the further requests, make sure you set the authorization field to -
Bearer < Token >