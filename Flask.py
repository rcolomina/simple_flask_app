''' HTTP Response Codes

200 OK
201 CREATED
400 BAD REQUEST
401 UNAUTHORIZED
403 FORBIDDEN
404 NOT FOUND
405 METHOD NOT ALLOWED
409 CONFLICT
500 INTERNAL SERVER ERROR

'''

from flask         import Flask, request,  make_response, jsonify, abort
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
def jsonify_output(data, status_code=200, headers=None, indent=4):
    print("debug:outputting in json format with status code "+str(status_code))
    print("hello data",data)
    resp = make_response(json.dumps(data,indent=indent), status_code)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['mimetype'] = 'application/json'
    resp.status_code = status_code
    print(resp.__dict__)
    return resp

# Define error handler for a bad request
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify_output({"status":405,
                           "message":"HTTP Method not Allowed for Request."},405)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify_output({"status":404,
                           "message":"Resource Not Found or Not Available"},404)    
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify_output({"status":500,
                           "message":"INTERNAL SERVER ERROR."},500)    
                          
@app.errorhandler(Exception) #werkzeug.exceptions)
def handle_error(error):
    print(type(error))
    
    if isinstance(error,werkzeug.exceptions.MethodNotAllowed):
        return jsonify_output({"status":405,
                               "message":"HTTP Method not Allowed for Request."},405)

    if isinstance(error,werkzeug.exceptions.NotFound):
        return jsonify_output({"status":404,
                               "message":"Resource Not Found or Not Available"},404)    

    if isinstance(error,sqlalchemy.exc.IntegrityError):
        return jsonify_output({"status":400,
                               "message":"INTEGRITY ERROR Duplicated Index or Null Key was provided."},400)

    # Anything else
    return jsonify_output({"status":500,
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
    return jsonify_output(data,status)

# Return Bad Request message configured
def output_bad_request(message):
    print("debug: output_bad_request")
    status = 400
    data = {"message":"BAD REQUEST "+message,"status":status}
    return jsonify_output(data,status)


def check_email_reg_exp(email):
    ''' Check whether email follows regular expression'''
    import re
    # If email is passed check regular expresion
    regexp="^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    if email != None and isinstance(email,str):
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",email):
            return True
    return False
    
def get_data_from_dict(mydict):
    ''' Return a tuple with the information required to build a contact '''
    print('debug: get_data_from_dict')    
    
    validKeys = ['username','email','firstname','surname']
    insersec  = [value for value in validKeys if value in mydict.keys()]
    if insersec != validKeys:
        return "INVALID_KEYS"

    username  = mydict['username']
    if username == None:
        return "NULL_KEY_ID"

    email     = mydict['email']                
    if not check_email_reg_exp(email):
        return "INVALID_EMAIL"

    print("hello")
    
    firstname = mydict['firstname']
    surname   = mydict['surname']

    # Create contact
    return (username,email,firstname,surname)
    

def string_on_extracted_data(extractData):
    print("debug: check extracted data")
    if isinstance(extractData,str):
        print("Extracted data is wrong")
        msg = "BAD DATA"
        if extractData == "USERNAME_NOT_IN_DATA":
            msg = "Username Primary Key NOT provided in Data Body JSON request."
        if extractData == "INVALID_KEYS":
            msg = "Invalid Keys in Data JSON request."
        if extractData == "NULL_KEY_ID":
            msg = "Null Primary Key was provided in Data JSON request."            
        if extractData == "INVALID_EMAIL":
            msg = "Invalid email"

        return (True,msg)
    else:
        print("Extracted data is good")
        return (False,"OK")
    
# This receives only POST method using json
@app.route('/contact/',methods=['POST'])
def post_contact():
    print("debug: post_contact")

    mydict={}
    try:
        ''' This functions only is used from POST and PUT routes
        This shoud try to get JSON content from request data
        otherwise return non JSON format '''
        mydict = request.get_json()  
    except:
        return output_bad_request("Data is not in JSON format.")

    if mydict == {}:
        return output_bad_request("Void JSON was given provided.")
    
    extractData = get_data_from_dict(mydict)
    badData,msg = string_on_extracted_data(extractData)    
    print(badData,msg)
    if badData:
        return output_bad_request(msg)
        
    # Add new contact to db
    db_session.add(Contact(extractData[0],
                           extractData[1],
                           extractData[2],
                           extractData[3]))
    db_session.commit()

    # Return OK message
    message ="OK New Contact With Username '"+extractData[0]+"' Added into the Database."
    status = 200
    data = {"message":message,"status":status}
    return jsonify_output(data,status)
    

@app.route('/contact/',methods=['GET']) 
def get_all_contact():
    # Querying contact matching username
    print("debug: get_all_contacts")
    myQueryContact = Contact.query.all()
    listOfContacts=[]
    if len(myQueryContact) > 0:
        for query in myQueryContact:
            listOfContacts.append(query.toDict())

        status = 200 
        data = {"status":status,"contacts":listOfContacts}     
        return jsonify_output(data, status)    
    else:
        abort(404)
    
@app.route('/contact/<username>',methods=['GET']) 
def get_single_contact(username):
    print('debug: get_single_contact')
    # Querying contact matching username
    #print(db_session.__dict__)
    
    myQueryContact = Contact.query.filter(Contact.username == username).first()    

    if myQueryContact != None:
        status = 200
        return jsonify_output(myQueryContact.toDict(),status)
    else:
        return output_not_found(username)

@app.route('/contact/<username>',methods=['PUT'])
def update_single_contact(username):
    print("debug: updating single contact")
    myQueryContact = Contact.query.filter(Contact.username == username).first()    
    if myQueryContact != None:

        mydict={}
        try:
            ''' This functions only is used from POST and PUT routes
            This shoud try to get JSON content from request data
            otherwise return non JSON format '''
            mydict = request.get_json()
            mydict['username'] = username
        except:
            return output_bad_request("Data not given in JSON format.")

        print(mydict)
        
        extractData = get_data_from_dict(mydict)
        badData,msg = string_on_extracted_data(extractData)
        if badData:
            return output_bad_request(msg)
                
        myQueryContact.email     = extractData[1]
        myQueryContact.firstname = extractData[2]
        myQueryContact.surname   = extractData[3]

        db_session.commit()

        message ="OK Contact was updated in the database."
        status = 201
        data = {"message":message,"status":status,
                "contact_updated":{"username":username,
                                   "email":myQueryContact.email,
                                   "firstname":myQueryContact.firstname,
                                   "surname":myQueryContact.surname}}
        
        return jsonify_output(data,status)
    else:
        return output_not_found(username)





@app.route('/contact/<username>',methods=['DELETE'])
def delete_single_contact(username):
    print("debug: Deleting single contact")
    print("debug: URI username:",username)

    #session = db_session()
    myQueryContact = Contact.query.filter(Contact.username == username).first()
    #print(myQueryContact)
    if myQueryContact != None:

        myQuery = Contact.query.filter(Contact.username == username)
        #print(myQuery)
        myQuery.delete()
        db_session.commit()

        message ="DELETE Contact from database."
        status = 200
        data = {"message":message,"status":status}
        return jsonify_output(data,status)
    else:
        return output_not_found(username)















