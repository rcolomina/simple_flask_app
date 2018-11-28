import os
import Flask as flask
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
        assert rv.get_json()['status'] == 404
        assert rv.get_json()['message'] == "Resource Not Found or Not Available."
        
        rv = self.app.get('/contact/nonavailable/resource')
        assert rv.get_json()['status'] == 404
        assert rv._status == '404 NOT FOUND'
        assert rv.get_json()['message'] == "Resource Not Found or Not Available."
        
    def test_post(self):
        print("Testing: POST method with single user")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})

        assert rv.get_json()['message'] == "Contact inserted succesfully in the database. ( Username = smith1 )"
        assert rv.get_json()['status'] == 200
        
        print("Testing: POST when data has missing non null argument")
        rv = self.app.post('/contact/',
                           json={"username":"smithd1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh"})
        #print(get_json()['status'])
        assert rv.get_json()['status'] == 400

        print("Testing: POST when existing username")
        rv = self.app.post('/contact/',
                           json={"username":"smith1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})
        json_data = rv.get_json()
        #print(json_data)
        assert json_data['message'] == "Integrity Error due to Duplicated Index or Null Key was provided."
        assert rv.get_json()['status'] == 400

        

    def test_get_username(self):
        
        # Insert a contact to have something in the database
        rv = self.app.post('/contact/',
                           json={"username":"smithdsa1",
                                 "email":"smith@gmail.com",
                                 "firstname":"Jonh",
                                 "surname":"Smith"})

        print("Testing: GET contact by username")
        rv = self.app.get('/contact/smithdsa1')
        assert rv.get_json()['status'] == 200        
        assert rv.get_json()['message'] == "Specific Contact retrieved succesfully from the database."
        
        print("Testing: Get Single Contact by missing Username")
        rv = self.app.get('/contact/smithdsa1dasds')
        assert rv.get_json()['status'] == 404
        assert rv.get_json()['message'] == "Contant Not Found in database. Username 'smithdsa1dasds' does not exist."
        
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

        assert json_data["contacts"][0]["username"]  == 'smithdsa1'
        assert json_data["contacts"][0]["email"]     == 'smith@gmail.com'
        assert json_data["contacts"][0]["firstname"] == 'Jonh'
        assert json_data["contacts"][0]["surname"]   == 'Smith'
         
        assert rv.get_json()['status'] == 200
              
    def test_delete_user(self):
        print("Testing: Delete a User")
        
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
        assert rv.get_json()['status'] == 200
        assert rv.get_json()["message"] == "Contact deleted from the database."
        
        rv = self.app.delete('/contact/beaton')
        assert rv.get_json()['status'] == 200
        assert rv.get_json()["message"] == "Contact deleted from the database."
        
        print("Testing: Get deleted contact by username")
        rv = self.app.get('/contact/smith')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()["message"] == "Contant Not Found in database. Username 'smith' does not exist."
        
        rv = self.app.delete('/contact/smithd')
        assert rv.get_json()['status'] == 404        
        assert rv.get_json()["message"] == "Contant Not Found in database. Username 'smithd' does not exist."


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
