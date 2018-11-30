# Simple Flask APP to Register Contact Details

This is simple Flask App using best practices and reusable code including unit testing. This is a simple app to register in a database contacts datails.

RESTfull architecture rules have been followed using JSON as interchagable format. Its specifications for its database were SQLAlchemy plus Sqlite3 as backend. 

## Download APP

$ git clone https://github.com/rcolomina/simple_flask_app

$ cd simple_flask_app

## Installation

This requires python3 and pip to install its dependencies.

### Install python3

$ apt-get install python3

### Install pip

$ apt-get install python3-pip

### Create a Virtual Environment inside this folder

$ python3 -m venv env

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

### URI:

'/contact/'

### Data (example):

{
"username":"myexampleusername",

"email":["exampleemail1@host1.com",
         "exampleemail2@host2.com",
         "exampleemail3@host3.com"],

"firstname":"examplefirstname",

"surname":"examplesurname"
}



Saving a contact a contact                    POST         Existing  username             200
   Saves a contact                    POST         Null      argument             400 
   Returns contact by username        GET          Existing  username             200
   Returns contact by username        GET          Missing   username             404
   Returns all contacts               GET          Exist at leas one username     200
   Returns all contacts               GET          Database is void               404
   Returns contacts by email          GET          Existing Email                 200
   Returns contacts by email          GET          Missing  Email                 404
   Delete existing user               DELETE       Existing username              200
   Delete non existing user           DELETE       Missing  username              404
   Update contact                     PUT          Existing username              200
   Update contact                     PUT          Missing  username              200


# Testing Flask API

You would need python unittest library to execute off-line testing on HTTP operations. An independent temporal database is created in the temporal folder

Local temporal sqlite database: 'sqlite:////tmp/flask_unittest.db'

Multiple assertions over the app source code accross different methods are verified by 'flask_test.py' module based on python unittest.

To run all of these previous test first verify you have loaded your python environment

$ source env/bin/activate

Launch all the test inside the app testing module

$ python flask_test.py

You can also run them separately by HTTP method

### To check unavailable operations

$ python -m unittest -q flask_test.FlaskTestCase.test_unavailable_resource

### To check POST methods to insert a contact

$ python -m unittest -q flask_test.FlaskTestCase.test_post

### To check GET methods to obtain a contact by username

$ python -m unittest -q flask_test.FlaskTestCase.test_get_username

### To check GET methods to obtain a contact by email

$ python -m unittest -q flask_test.FlaskTestCase.test_get_by_username

### To check GET methods to obtain all contacts

$ python -m unittest -q flask_test.FlaskTestCase.test_get_all

### To check GET methods to obtain contacts by email

$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email

### To check DELETE method 

$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email


### To check UPDATE method