import os
import Flask as flask
#from Flask import setup_sqlalchemy_database_uri 
import unittest
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

    def test_empty_root(self):
        rv = self.app.get('/')        
        assert rv._status == '404 NOT FOUND'
        assert rv._status_code == 404

    def test_post(self):
        print("testing: Test post single user")
        rv = self.app.post('/contact/',
                           json={"username":"rcolomina1",
                                 "email":"rcolomina@gmail.com",
                                 "firstname":"Ruben",
                                 "surname":"Colomina"})
        
        json_data = rv.get_json()
        assert rv._status_code == 200
        
        print("Testing: test post 2 - Missing non null argument")
        rv = self.app.post('/contact/',
                           json={"username":"rcolomina1",
                                 "email":"rcolomina@gmail.com",
                                 "firstname":"Ruben"})
        assert rv._status_code == 400


    def test_get_username(self):
        # Insert a contact to have something in the database
        rv = self.app.post('/contact/',
                           json={"username":"rcolomindsa1",
                                 "email":"rcolomina@gmail.com",
                                 "firstname":"Ruben",
                                 "surname":"Colomina"})

        print("Testing: Get Single Contact by Username")
        rv = self.app.get('/contact/rcolomindsa1')
        assert rv._status_code == 200
        
    def test_get_all(self):
        # Insert a contact to have something in the database
        print("Testing: Get All Contacts")
        
        rv = self.app.post('/contact/',
                           json={"username":"rcolomindsa1",
                                 "email":"rcolomina@gmail.com",
                                 "firstname":"Ruben",
                                 "surname":"Colomina"})
        
        rv = self.app.get('/contact/')
        assert rv._status_code == 200
              

    def test_delete_user(self):
        print("Testing: Delete A User")
        
        rv = self.app.post('/contact/',
                           json={"username":"rcolomina",
                                 "email":"rcolomina@gmail.com",
                                 "firstname":"Ruben",
                                 "surname":"Colomina"})
        
        rv = self.app.delete('/contact/rcolomina')
        #print(rv)
        assert rv._status_code == 204

        
        
if __name__ == '__main__':
    unittest.main()
