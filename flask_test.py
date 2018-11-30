import os
import Flask as flask
import unittest
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

##  Operation                          ## Method    ## Test Cases        ## Expected status code
#   Non supported                      POST    '/' URI                              404
#   Non supported                      POST    /contact/nonavailable/resource' URI  404
#   Saves a contact                    POST    New       username                   200
#   Saves a contact                    POST    Existing  username                   400
#   Saves a contact                    POST    Null      argument                   400
#   Saves a contact multiple emails    POST    Existing  argument                   400

#   Returns contact by username        GET     Existing  username                   200
#   Returns contact by username        GET     Missing   username                   404
#   Returns all contacts               GET     Exist at leas one username           200
#   Returns all contacts               GET     Database is void                     404
#   Returns contacts by email          GET     Existing Email                       200
#   Returns contacts by email          GET     Missing  Email                       404
#   Delete existing user               DELETE  Existing username                    200
#   Delete non existing user           DELETE  Missing  username                    404
#   Update contact                     PUT     Existing username                    200
#   Update contact                     PUT     Missing  username                    200
#   Update contact                     PUT     Several emails updated               200

#   Overall notice that internal server errors should return 500

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        print("Testing: Setup App Data Base ")

        # Temporal database 
        temp_database_uri = 'sqlite:////tmp/flask_unittest.db'

        # Setup temporal database on flask
        flask.engine     = create_engine(temp_database_uri, convert_unicode=True)
        flask.DBSession  = sessionmaker(autocommit=False,autoflush=False,bind=flask.engine)
        flask.db_session = scoped_session(flask.DBSession)
        
        # Dropall previous data before testing in temporal database
        flask.Base.metadata.drop_all(bind=flask.engine)

        print("debug:",flask.engine)        
        flask.app.testing = True

        # Setup app test client
        self.app = flask.app.test_client()
        with flask.app.app_context():
            flask.setup()  # initialize database

    def tearDown(self):
        print("Testing: Clossing down database")
        flask.db_session.remove()

        
    def test_unavailable_resource(self):
        print("Testing: POST method non supported")
        rv = self.app.get('/')        
        assert rv._status == '404 NOT FOUND'
        assert rv.get_json()['status']  == 404
        assert rv.get_json()['message'] == "Resource Not Found or Not Available."

        print("Testing: POST method non supported")
        rv = self.app.get('/contact/nonavailable/resource')
        assert rv.get_json()['status']  == 404
        assert rv.get_json()['message'] == "Resource Not Found or Not Available."

    def test_post(self):
        print("Testing: POST method new username")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"John",
                                 "surname":"Smith"})

        assert rv.get_json()['message'] == "Contact inserted succesfully in the database. ( Username = smith1 )"
        assert rv.get_json()['status'] == 200
        
        print("Testing: POST when null argument")
        rv = self.app.post('/contact/',
                           json={"username":"jsmith",
                                 "email":"smith@gmail.com",
                                 "firstname":"John"})

        assert rv.get_json()['status']  == 400
        #print(rv.get_json()['message'])
        assert rv.get_json()['message'] == "Bad Request. Invalid Keys in Data JSON request."
                
        print("Testing: POST method existing username")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":["smith@gmail.com","smith@hotmail.com"],
                                 "firstname":"John",
                                 "surname":"Smith"})

        #print("hello ->",rv.get_json()['message'])
        assert rv.get_json()['message'] == "Integrity Error due to Duplicated Index or Null Key was provided."
        assert rv.get_json()['status'] == 400


        print("Testing: POST new user with multiple emails")
        rv = self.app.post('/contact/',
                           json={"username":"jsmith",
                                 "email":["smith@gmail.com","smith@hotmail.com"],
                                 "firstname":"John",
                                 "surname":"Smith"})

        assert rv.get_json()['message'] == "Contact inserted succesfully in the database. ( Username = jsmith )"
        print(rv.get_json()['message'])
        assert rv.get_json()['status'] == 200
        


    def test_get_by_username(self):

        print("Testing: GET contact by username")
        
        # This test requires POST method works
        rv = self.app.post('/contact/',
                           json={"username":"jsmith123",
                                 "email":["smith123@gmail.com","smith123@hotmail.com"],
                                 "firstname":"John",
                                 "surname":"Smith"})
        
        rv = self.app.get('/contact/jsmith123')
        assert rv.get_json()['status'] == 200        
        assert rv.get_json()['message'] == "Specific Contact retrieved succesfully from the database."
        
        print("Testing: Get contact by a missing username")
        rv = self.app.get('/contact/smithdsa1dasds')
        assert rv.get_json()['status'] == 404
        print(rv.get_json()['message'])
        assert rv.get_json()['message'] == "Contant Not Found in database. Username 'smithdsa1dasds' does not exist."

        
                
    def test_get_all(self):
        print("Testing: Get All Contacts")

        # Insert a contact to have something in the database
        rv = self.app.post('/contact/',
                           json={"username":"smithdsa1",
                                 "email":["smith@gmail.com",
                                          "smith3@hotmail.com"],
                                 "firstname":"John",
                                 "surname":"Smith"})

        rv = self.app.post('/contact/',
                           json={"username":"johnlennon",
                                 "email":["jlennon@gmail.com",
                                          "jlennon@hotmail.com"],
                                 "firstname":"John",
                                 "surname":"Lennon"})
        
        rv = self.app.get('/contact/')
        json_data = rv.get_json()

        assert json_data["contacts"][0]["username"]  == 'smithdsa1'
        assert json_data["contacts"][0]["email"]     == ["smith@gmail.com",
                                                         "smith3@hotmail.com"]
        assert json_data["contacts"][0]["firstname"] == 'John'
        assert json_data["contacts"][0]["surname"]   == 'Smith'

        assert json_data["contacts"][1]["username"]  == 'johnlennon'
        assert json_data["contacts"][1]["email"]     == ['jlennon@gmail.com',
                                                         'jlennon@hotmail.com']
        assert json_data["contacts"][1]["firstname"] == 'John'
        assert json_data["contacts"][1]["surname"]   == 'Lennon'
        
        assert rv.get_json()['status'] == 200

        
    def test_get_contacts_by_email(self):
        print("Testing: Get contacts by email")

        # Insert contacts to have something in the database
        rv = self.app.post('/contact/',
                           json={"username":"jsmith",
                                 "email":["jsmith@gmail.com",
                                          "jsmith@hotmail.com",
                                          "asmith@gmail.com"],
                                 "firstname":"John",
                                 "surname":"Smith"})

        rv = self.app.post('/contact/',
                           json={"username":"asmith",
                                 "email":["asmith@gmail.com",
                                          "asmith@hotmail.com",
                                          "jsmith@gmail.com"],
                                 "firstname":"Ada",
                                 "surname":"Smith"})

        
        rv = self.app.post('/contact/',
                           json={"username":"amybeaton",
                                 "email":["abeaton@gmail.com",
                                          "abeaton@hotmail.com"],
                                 "firstname":"Amy",
                                 "surname":"Beaton"})
        
        
        rv = self.app.get('/contact/email/asmith@gmail.com')
        assert rv.get_json()['status']   == 201
        assert rv.get_json()['message']  == 'Contacts retrieved succesfully from the database by email'
        assert rv.get_json()['contacts'] ==  [{'username': 'jsmith',
                                               'email': ['jsmith@gmail.com',
                                                         'jsmith@hotmail.com',
                                                         'asmith@gmail.com'],
                                               'firstname': 'John',
                                               'surname': 'Smith'},
                                              {'username': 'asmith',
                                               'email': ['asmith@gmail.com',
                                                         'asmith@hotmail.com',
                                                         'jsmith@gmail.com'],
                                               'firstname': 'Ada',
                                               'surname': 'Smith'}]


        print("Testing: Get contacts by email with bad format")
        rv = self.app.get('/contact/email/asmithgmail.com')
        assert rv.get_json()['status']   == 400
        assert rv.get_json()['message']  == 'Invalid email pattern found.'
        
        print("Testing: Get contacts by email returns same contact for all emails")
        rv1 = self.app.get('/contact/email/abeaton@hotmail.com')
        rv2 = self.app.get('/contact/email/abeaton@gmail.com')
        assert rv1.get_json()["contacts"] == rv2.get_json()["contacts"]

        
        
    def test_delete_user(self):
        print("Testing: Delete a User")
        
        rv = self.app.post('/contact/',
                           json={"username":"smith",
                                 "email":"jsmith@gmail.com",
                                 "firstname":"John",
                                 "surname":"Smith"})

        rv = self.app.post('/contact/',
                           json={"username":"beaton",
                                 "email":["hbeaton@gmail.com",
                                          "abeaton@hotmail.com"],
                                 "firstname":"Henry",
                                 "surname":"Beaton"})

        rv = self.app.post('/contact/',
                           json={"username":"amybeaton",
                                 "email":["abeaton@gmail.com",
                                          "abeaton@hotmail.com"],
                                 "firstname":"Amy",
                                 "surname":"Beaton"})

        # Try to delete again
        print("Testing: Delete already deleted contacts")

        rv = self.app.delete('/contact/smith')
        assert rv.get_json()['status'] == 200
        assert rv.get_json()["message"] == "Contact deleted from the database."
        
        rv = self.app.delete('/contact/beaton')
        assert rv.get_json()['status'] == 200
        assert rv.get_json()["message"] == "Contact deleted from the database."

        # Try to get deleted contacts
        print("Testing: Get deleted contact by username")
        rv = self.app.get('/contact/smith')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()["message"] == "Contant Not Found in database. Username 'smith' does not exist."        
        rv = self.app.delete('/contact/smithd')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()["message"] == "Contant Not Found in database. Username 'smithd' does not exist."

        # Check that usernames deleted does not exist in the database
        rv = self.app.get('/contact/beaton')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()['message'] == "Contant Not Found in database. Username 'beaton' does not exist."
        
        rv = self.app.get('/contact/smithd')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()['message'] == "Contant Not Found in database. Username 'smithd' does not exist."

        rv = self.app.get('/contact/smith')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()['message'] == "Contant Not Found in database. Username 'smith' does not exist."

        
    def test_method_not_allowed(self):
        print("Testing: Method not allowed")

        rv = self.app.post('/contact/beaton',
                           json={"username":"beaton",
                                 "email":"hbeaton@gmail.com",
                                 "firstname":"Henry",
                                 "surname":"Beaton"})
        assert rv.get_json()['status'] == 405
        assert rv.get_json()["message"] == "HTTP Method was Not Allowed for the Request."

            
if __name__ == '__main__':
    unittest.main()
