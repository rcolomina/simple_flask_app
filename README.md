# Simple Flask APP to Register Contact Details

This is simple Flask App using best practices and reusable code including unit testing. This is a simple app to register in a database contacts datails.

RESTfull architecture rules have been followed using JSON as interchagable format. Its specifications for its database were SQLAlchemy plus Sqlite3 as backend. 

## Download the project folder

To download this project you will need git to clone it on your machine.

$ git clone https://github.com/rcolomina/simple_flask_app

$ cd simple_flask_app

## Installation

This requires python3 and pip to install its dependencies.

### Install python3

$ apt-get install python3

### Install pip

$ apt-get install python3-pip

### Create a Virtual Environment inside the project folder

$ cd simple_flask_app

$ python3 -m venv testing_env

### Activate your virtual environment

$ source env/bin/activate

### Install dependencies Using PIP

$ pip install -r requirements.txt

## App Data Base Model

The data base model contains two related tables one to many.

A first one named 'contacts' which contains:

Contact(id, username, email, firstname, surname)

The field 'username' is the primary key. Fields 'email', 'firstname' and 'surname' were defined as non nullable.

A second table named 'emails' which is a child from the first one contains:

Email(id, username, email)

The filed 'username' in 'emails' table is a foreigh key of 'contacts'.

## SQL ALchemy API and Sqlite3

The specificatoins for the database on this app are SQL ALchemy plus SQLITE3.

SQL Alchemy is an API for databases allowing abstractions on SQL, which means that all the entities and relationships among tables on your database are handled by python classes. Therefor the programmer does not have to worry about sql embbeded code. This uses sqlite3 which has limitations but it is good enough for the purpose of the app.

# Flask API Usage

This is a RESTful API based on JSON format. See its HTTP operations below.

## POST Method for to include a new Contact and Email

To post (insert) a new contact use the following URI and data in JSON format:

### URIs availables

Method  URL                  Operation

------

POST '/contact/'             Insert a new contact in the data base

PUT  '/contact/<username>'   Update a contact with specific username

GET  '/contact/'             Returns all contacts in the data base

GET  '/contact/<username>'   Returns a contact with specific username
 
GET  '/contact/email/<email>' Returns all contacts with specific email

DELETE '/contact/<username>' Delete a contact with specific username

### Data Format

JSON format is used to POST and PUT content Data. As an example to do data posting:

```
{"username":"fbolson",
"email":["frodobolson@mordor.com","fbolson@earth.com"],
"firstname":"Frodo",
"surname":"BolsonCerrado"}"
```

Notice that email admits list of emails. "email" contact can be either a string or a list of strings. The format of each email is checked with the regular expresion as follows:

```
^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$
```

# Testing Flask API

## Python Unit test 

You would need python unittest library to execute off-line testing on HTTP operations. An independent temporal database is created in the temporal folder

Local temporal sqlite database: 

'sqlite:////tmp/flask_unittest.db'

Multiple assertions over the app source code accross different HTTP methods are verified by the module 'flask_test.py' based on python unittest.

To run all of these test within the previous module firstly verify you have loaded your python environment.

$ source env/bin/activate

Launch all the test inside the app testing module

$ python flask_test.py

## CURL testing

Also you can also run them separately by HTTP method depending on the purpose:

$ python -m unittest -q flask_test.FlaskTestCase.test_unavailable_resource
$ python -m unittest -q flask_test.FlaskTestCase.test_method_not_allowed
$ python -m unittest -q flask_test.FlaskTestCase.test_post
$ python -m unittest -q flask_test.FlaskTestCase.test_get_username
$ python -m unittest -q flask_test.FlaskTestCase.test_get_by_username
$ python -m unittest -q flask_test.FlaskTestCase.test_get_all
$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email
$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email

Additionaly curl library can also be used to test this app. Taylored scripts are available for this.

You should launch your app first of all:

$ ./env_flask.sh

Now you can launch commands to it with curl. As example you can POST a contact as follows:

$ ./test_curl_post_username.sh jsmith jsmith@gmail.com John Smith




# Authors

* **Ruben Colomina Citoler**

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.

