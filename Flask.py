''' HTTP Response Codes

200 OK
201 CREATED
204 NO CONTENT
400 BAD REQUEST
401 UNAUTHORIZED
403 FORBIDDEN
404 NOT FOUND
405 METHOD NOT ALLOWED
409 CONFLICT
500 INTERNAL SERVER ERROR

'''

from flask         import Flask, request,  make_response, jsonify
from flask_restful import Api

from models import Base, Contact

import json
import werkzeug
import sqlalchemy

#from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialize Flask Application
app = Flask(__name__)

from config import Config

# Default configurataion for the app
app.config['SQLALCHEMY_DATABASE_URI']        = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Create API from this app
api = Api(app)

#db = SQLAlchemy(app)
#DBSession  = sessionmaker(autocommit=False,autoflush=False,bind=engine)
#db_session = scoped_session(DBSession)
#db_session=db.session

## CREATE ENGINE and SESSION using the declarative way
sqlalchemy_database_uri = app.config['SQLALCHEMY_DATABASE_URI']
engine                  = create_engine(sqlalchemy_database_uri, convert_unicode=True)
DBSession               = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db_session              = scoped_session(DBSession)

@app.before_first_request
def setup():
    print("debug: setup app")
    # Binding Base Model class to the engine
    #Base.metadata.drop_all(bind=engine)
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    print("debug:",engine)
    
# Define Api representation
@api.representation('application/json')
def output_json(data, status_code=200, headers=None, indent=4):
    resp = make_response(json.dumps(data,indent=indent), status_code)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['mimetype'] = 'application/json'
    resp.status_code = status_code
    return resp

# Define error handler for a bad request
@app.errorhandler(Exception) #werkzeug.exceptions)
def handle_error(error):
    #print(type(error))

    if isinstance(error,werkzeug.exceptions.MethodNotAllowed):
        return output_json({"status":405,
                            "message":"HTTP Method not Allowed for Request."},405)

    if isinstance(error,werkzeug.exceptions.NotFound):
        return output_json({"status":404,
                            "message":"Resource Not Found or Not Available"},404)    

    if isinstance(error,sqlalchemy.exc.IntegrityError):
        return output_json({"status":400,
                            "message":"INTEGRITY ERROR Duplicated Index or Null Key was provided."},400)    

    return output_json({"status":500,
                        "message":"INTERNAL SERVER ERROR."},500)    


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

########################
# DEFINE FLASK ROUTES
########################

# Not Found message configured
def output_not_found(username):
    message = "NOT FOUND Contact with username '"+username+"' was not found in the database."
    status = 404
    data = {"message":message,"status":status}
    return output_json(data,status)

# Return Bad Request message configured
def output_bad_request(message):
    status = 400
    data = {"message":"BAD REQUEST "+message,"status":status}
    return output_json(data,status)

# Check if request data was given in JSON 
def get_dict_from_request(request):
    print('debug: get_dict_from_request')
    try:
        return request.get_json()  
    except:
        return output_bad_request("Data not given in JSON format.")

def check_email_reg_exp(email):
    import re
    # If email is passed check regular expresion
    regexp="^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    if not re.match(regexp,email):
        return output_bad_request("Email does not match the regular expresion"+regexp)
    else:
        return True
    
def get_data_from_dict(mydict):
    print('debug: get_data_from_dict')
    # Extract keys
    keys      = mydict.keys()
    # Initialize contact
    username, email, firstname, surname  = None,None,None,None
        
    if 'username' in keys:                        
        username  = mydict['username']
    else:
        return output_bad_request("Primary Key not provided in JSON request")
        
    if 'email' in keys:
        email     = mydict['email']        
        if email != None:
            check_email_reg_exp(email)
                
    if 'firstname' in keys:            
        firstname = mydict['firstname']
            
    if 'surname' in keys:
        surname   = mydict['surname']

    # Create contact
    return username,email,firstname,surname
    

# This receives only POST method using json
@app.route('/contact/',methods=['POST'])
def post_contact():
    print("debug: post_contact")
    #print(request.__dict__)
    mydict = get_dict_from_request(request)
    #print(mydict)
    username,email,firstname,surname = get_data_from_dict(mydict)
    #print(username,email,firstname,surname)

    # Add new contact to db
    db_session.add(Contact(username,email,firstname,surname))
    db_session.commit()

    # Return OK message
    message ="OK New Contact With Username '"+username+"' Added into the Database."
    status = 200
    data = {"message":message,"status":status}
    #print(data)
    return output_json(data,status)
    

@app.route('/contact/',methods=['GET']) 
def get_all_contact():
    # Querying contact matching username
    print("debug: get_all_contacts")
    myQueryContact = Contact.query.all()
    #print(myQueryContact)
    listOfContacts=[]
    #print("len",len(myQueryContact))
    if len(myQueryContact) > 0:
        #print(myQueryContact)
        for query in myQueryContact:
            #print(query)
            #print("query.username",query.username)
            #print(type(query))
            #print(query.toDict())
            listOfContacts.append(query.toDict())
        #return "OK"
        status = 200 
        data = {"status":status,"contacts":listOfContacts}     
        return output_json(data, status)
    
    else:
        message = "NOT DATA FOUND in the database."
        status  = 404
        data = {"message":message,"status":status}
        return output_json(data,status)
    
@app.route('/contact/<username>',methods=['GET']) 
def get_single_contact(username):
    print('debug: get_single_contact')
    # Querying contact matching username
    #print(db_session.__dict__)
    
    myQueryContact = Contact.query.filter(Contact.username == username).first()    

    if myQueryContact != None:
        status = 200
        return output_json(myQueryContact.toDict(),status)
    else:
        return output_not_found(username)

@app.route('/contact/<username>',methods=['PUT'])
def update_single_contact(username):
    print("debug: updating single contact")
    myQueryContact = Contact.query.filter(Contact.username == username).first()    
    if myQueryContact != None:

        #print(myQueryContact)
        #print("username  found: "+myQueryContact.username)
        #print("email     found: "+myQueryContact.email)
        #print("surname   found: "+myQueryContact.surname)
        #print("firstname found: "+myQueryContact.firstname)
        
        mydict = get_dict_from_request(request)
        #print(mydict)

        key="email"
        if key in mydict.keys():
            email = mydict[key]            
            if email != None:
                check_email_reg_exp(email)
                myQueryContact.email     = email

        print("username  found: "+myQueryContact.username)
        print("email     found: "+myQueryContact.email)

        def get_value_from_dict(key,mydict,previous):
             if key in mydict.keys():
                 if mydict[key] != None:
                     return mydict[key]
                     
             return previous
        
        myQueryContact.firstname = get_value_from_dict("firstname",mydict,myQueryContact.firstname)
        myQueryContact.surname   = get_value_from_dict("surname",mydict,myQueryContact.surname)

        db_session.commit()

        message ="OK Contact was updated in the database."
        status = 201
        data = {"message":message,"status":status,
                "contact_updated":{"username":username,
                                   "email":myQueryContact.email,
                                   "firstname":myQueryContact.firstname,
                                   "surname":myQueryContact.surname}}
        
        return output_json(data,status)
    else:
        return output_not_found(username)





@app.route('/contact/<username>',methods=['DELETE'])
def delete_single_contact(username):
    print("debug: Deleting single contact")
    print("debug: URI username:",username)

    #session = db_session()
    myQueryContact = Contact.query.filter(Contact.username == username) #.first()
    print(myQueryContact)
    if myQueryContact != None:
        
        myQueryContact.delete()
        db_session.commit()

        message ="DELETE Contact from database."
        status = 204
        data = {"message":"DELETE "+message,"status":status}
        return output_json(data,status)
    else:
        return output_not_found(username)















