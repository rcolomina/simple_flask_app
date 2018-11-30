# Simple Flask APP to Register Contact Details

This is simple RESTfull Flask App to register contact details on its database. JSON is the only interchagable format used by this app. 

## Installation

This requires python3 and pip to install its dependencies from requirements.txt.

### Install python3

```
$ apt-get install python3
```

### Install pip

```
$ apt-get install python3-pip
```

### Create a Virtual Environment inside the project folder

```
$ cd simple_flask_app

$ python3 -m venv testing_env
```

### Activate your virtual environment
```
$ source testing_env/bin/activate
```

### Install dependencies Using PIP
```
$ pip install -r requirements.txt
```
### Running this Flask Application

Export the following environment variables
```
$export FLASK_ENV=development
$export FLASK_APP=Flask.py
$ flask run 
```

Alternatively there is a script which launch these three commands of above for you

$ ./env_flask.sh

The application will run on the default Flask IP and PORT

```
127.0.0.1:5000
```

At this moment you should open another terminal to launch HTTP commands againts the application or used a web brower to test some API request on the URL by default. If this the first time you run the app a database will create in the project folder. Its name is defined by the python configuration file. When you close the app the data will persist on this database.

Every time you run your application again the database configured will be loaded containing allr previously inseted data. It is possible to drop all tables activating a flag in the configuration file. This will reset all content of the database.



# App Configuration File

This configuration file contains parameters such as FLASK IP and PORT, SQLALCHEMY and SQLITE name and its location.

Also it is possible to configure the regular expression which will parse the emails passed within the contact details.

Additionaly it is possible to configure output messages that are returned by HTTP responses. You can modify these to other language for instance.

# Flask API Usage

This is a RESTful API based on interchange of JSON formats. Its HTTP operations are in the section below.

### HTTP Methods and URL availables

HTTP methodss along with URL allow different  operation to perform againts the database. These are as follows:

```
Method  URL                     Operation
------  ----------------------  -----------------------------------------
POST    /contact/               Insert a new contact in the data base
PUT     /contact/<username>     Update a contact with specific username
GET     /contact/               Returns all contacts in the data base
GET     /contact/<username>     Returns a contact with specific username
GET     /contact/email/<email>  Returns all contacts with specific email
DELETE  /contact/<username>     Delete a contact with specific username
```

You can also see the routes available from the application running the command:

$ flask routes

So you will get the following ones

```
Endpoint               Methods  Rule
---------------------  -------  -----------------------
delete_single_contact  DELETE   /contact/<username>
get_all_contact        GET      /contact/
get_contacts_by_email  GET      /contact/email/<email>
get_single_contact     GET      /contact/<username>
post_contact           POST     /contact/
static                 GET      /static/<path:filename>
update_single_contact  PUT      /contact/<username>
```

### Data Format

JSON format is the only format used on this API. To POST and PUT JSON content Data must be prepared.  As follows you can see an example as schema for posting a contact with multiple emails.

```
{"username":"fbolson",
"email":["frodobolson@mordor.com","fbolson@earth.com"],
"firstname":"Frodo",
"surname":"BolsonCerrado"}"
```

Notice that email admits list of emails. "email" contact can be either a string or a list of strings. The format of each email is checked againts a regular expresion specified in the configuration file having the following string:

```
^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$
```

# Testing Flask API

This API can be tested using the python unit test module or via shell script which use curl command. 

## Python Unit Test 

The standard python module unittest has been used to execute HTTP operations againts the app. An independent temporal database is created for this purpose in the temporal folder.

Local temporal sqlite database: 

```
sqlite:////tmp/flask_unittest.db
```

Multiple assertions over the app source code accross different HTTP methods are verified by the module 'flask_test.py' based on python unittest.

To run all of these test within the previous module firstly verify you have loaded your python environment.

$ source testing_env/bin/activate

Launch all the test inside the app testing module

$ python flask_test.py

Also you can also run them separately by HTTP method depending on the purpose:

```
$ python -m unittest -q flask_test.FlaskTestCase.test_unavailable_resource
$ python -m unittest -q flask_test.FlaskTestCase.test_method_not_allowed
$ python -m unittest -q flask_test.FlaskTestCase.test_post
$ python -m unittest -q flask_test.FlaskTestCase.test_get_username
$ python -m unittest -q flask_test.FlaskTestCase.test_get_by_username
$ python -m unittest -q flask_test.FlaskTestCase.test_get_all
$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email
$ python -m unittest -q flask_test.FlaskTestCase.test_get_contacts_by_email
```

## CURL testing

Additionaly curl library can also be used to test this app. Taylored scripts are available for this.

You should launch your app first of all:

$ ./env_flask.sh

Now you can launch commands to it with curl. As example you can POST a contact as follows:

$ ./test_curl_post_username.sh jsmith jsmith@gmail.com John Smith


## App Data Base Model

The data base model contains two related tables with a relationship one to many.

A first table named 'contacts' which contains:

```
Contact(id, username, email, firstname, surname)
```

The field 'username' is the primary key. Fields 'email', 'firstname' and 'surname' were defined as non nullable.

A second table named 'emails' which is a child from the first one contains:

```
Email(id, username, email)
```

The filed 'username' in 'emails' table is a foreigh key of 'contacts'.

## SQL ALchemy API and Sqlite3

The specificatoins for the database on this app are SQL ALchemy plus SQLITE3.

SQL Alchemy is an API for databases allowing abstractions on SQL, which means that all the entities and relationships among tables on your database are handled by python classes. Therefor the programmer does not have to worry about sql embbeded code. This uses sqlite3 which has limitations but it is good enough for the purpose of the app.

# Celery Testing


# Authors

* **Ruben Colomina Citoler**

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.

