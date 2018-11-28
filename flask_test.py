import os
import Flask as flask
#from Flask import setup_sqlalchemy_database_uri 
import unittest
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



##  Operation                              ## Test Cases                    ## Expected status code
#   Non supported                          GET  method '/' URI                        404
#   Saves a contact                        POST method existing username              200
#   Saves a non valid contact (nulls)      POST method missing   argument             400 
#   Saves an existing contact              POST method existing  username             400
#   Returns existing  contact by username  GET  method exisiting username             200
#   Returns missing contact                GET  method missing   username             404
#   Returns all contacts                   GET  method all usernames                  200
#   Delete existing user                   DELETE method on existing username         200
#   Delete non existing user               DELETE method missing username             404
class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        print("Testing: Setup App Data Base ")
        
        temp_database_uri = 'sqlite:////tmp/flask_unittest.db'

        # Setup temporal database on flask
        flask.engine     = create_engine(temp_database_uri, convert_unicode=True)
        flask.DBSession  = sessionmaker(autocommit=False,autoflush=False,bind=flask.engine)
        flask.db_session = scoped_session(flask.DBSession)
        # Dropall previous data before testing in temporal database
        flask.Base.metadata.drop_all(bind=flask.engine)

        print("debug:",flask.engine)
        
        flask.app.testing = True
        # Setup 
        self.app = flask.app.test_client()
        with flask.app.app_context():
            flask.setup()

    def tearDown(self):
        print("Testing: Clossing down database")
        #os.close(self.db_fd)
        #os.unlink(flask.app.config['DATABASE'])

    def test_unavailable_resource(self):
        rv = self.app.get('/')        
        assert rv._status == '404 NOT FOUND'
        assert rv._status_code == 404

        rv = self.app.get('/contact/nonavailable/resource')
        assert rv._status_code == 404
        assert rv._status == '404 NOT FOUND'
        
    def test_post(self):
        print("Testing: POST method with single user")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})
        
        json_data = rv.get_json()
        assert json_data['message'] == "OK New Contact With Username 'smith1' Added into the Database."
        
        print("Testing: POST when data has missing non null argument")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh"})
        assert rv._status_code == 400

        print("Testing: POST when existing username")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh","surname":"Smith"})
        json_data = rv.get_json()
        print(json_data)
        assert json_data['message'] == "INTEGRITY ERROR Duplicated Index or Null Key was provided."
        assert rv._status_code == 400

        

    def test_get_username(self):
        
        # Insert a contact to have something in the database
        rv = self.app.post('/contact/',
                           json={"username":"smithdsa1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})

        print("Testing: GET contact by username")
        rv = self.app.get('/contact/smithdsa1')
        assert rv._status_code == 200

        print("Testing: Get Single Contact by missing Username")
        rv = self.app.get('/contact/smithdsa1dasds')
        assert rv._status_code == 404

    def test_get_all(self):
        # Insert a contact to have something in the database
        print("Testing: Get All Contacts")
        
        rv = self.app.post('/contact/',
                           json={"username":"smithdsa1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})
        
        rv = self.app.get('/contact/')
        json_data = rv.get_json()
        #print(json_data)
        assert json_data["contacts"][0]["username"]  == 'smithdsa1'
        assert json_data["contacts"][0]["email"]     == 'smith@gmail.com'
        assert json_data["contacts"][0]["firstname"] == 'Jonh'
        assert json_data["contacts"][0]["surname"]   == 'Smith'
         
        assert rv._status_code == 200
              
    def test_delete_user(self):
        print("Testing DELETE a User")
        
        rv = self.app.post('/contact/',
                           json={"username":"smith",
                                 "email":"jsmith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})

        rv = self.app.post('/contact/',
                           json={"username":"beaton",
                                 "email":"hbeaton@gmail.com",
                                 "firstname":"Henry",
                                 "surname":"Beaton"})

        
        rv = self.app.delete('/contact/smith')
        assert rv._status_code == 200
        assert rv.get_json()["message"] == "DELETE Contact from database."
        
        rv = self.app.delete('/contact/beaton')
        assert rv._status_code == 200
        assert rv.get_json()["message"] == "DELETE Contact from database."
        
        print("Testing: Get deleted contact by username")
        rv = self.app.get('/contact/smith')
        assert rv._status_code == 404
        assert rv.get_json()["message"] == "NOT FOUND Contact with username 'smith' was not found in the database."
        
        rv = self.app.delete('/contact/smithd')
        assert rv._status_code == 404
        assert rv.get_json()["message"] == "NOT FOUND Contact with username 'smithd' was not found in the database."



    def test_method_not_allowed(self):
        print("Testing: Method not allowed")

        rv = self.app.post('/contact/beaton',
                           json={"username":"beaton",
                                 "email":"hbeaton@gmail.com",
                                 "firstname":"Henry",
                                 "surname":"Beaton"})

        print(rv.__dict__)
        #json_data = rv.get_json()["message"] 

    #def test_updated_iser(self):
            
if __name__ == '__main__':
    unittest.main()
