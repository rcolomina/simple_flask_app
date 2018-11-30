# Simple Flask APP

This is simple Flask App using best practices and reusable code including unit testing.

RESTfull architecture has been followed.

SQLAlchemy api within Sqlite3 as database backend

## Installation

You will require python and pip to install libraries dependencies on this application.

## Install python3

$ apt-get install python3

## Install pip

$ apt-get install python3-pip

## Create a virtual environment inside this folder

$ python3 -m venv env

## Activate your virtual environment

$ source env/bin/activate

## Data Base Model

The data base model contains two related tables.

A first table named 'contacts' contains:
Contact(id, username, email, firstname, surname)

A second table named 'emails' which is a child from the first one contains:
Email(id, username, email)


## API usage

This is a RESTful API based on JSON format. See its operations below.

# POST Method

To post (insert in database) a new contact use the following JSON format:

{
"username":"myexampleusername",
"email":["exampleemail1@host1.com","exampleemail2@host2.com","exampleemail3@host3.com"],
"firstname":"examplefirstname",
"surname":"examplesurname"
}

Saving a contact a contact                    POST         Existing  username             200
#   Saves a contact                    POST         Null      argument             400 
#   Returns contact by username        GET          Existing  username             200
#   Returns contact by username        GET          Missing   username             404
#   Returns all contacts               GET          Exist at leas one username     200
#   Returns all contacts               GET          Database is void               404
#   Returns contacts by email          GET          Existing Email                 200
#   Returns contacts by email          GET          Missing  Email                 404
#   Delete existing user               DELETE       Existing username              200
#   Delete non existing user           DELETE       Missing  username              404
#   Update contact                     PUT          Existing username              200
#   Update contact                     PUT          Missing  username              200
