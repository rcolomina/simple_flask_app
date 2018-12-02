# Flask modules
from flask         import Flask, request,  make_response, jsonify, abort
from flask_restful import Api

# SqlAlchemy modules
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

# Others
import json
import werkzeug

# Internal modules
from models import Base, Contact, Email
from aux_functions import output_not_found
from aux_functions import output_bad_request
from aux_functions import check_email_reg_exp
from aux_functions import get_data_from_dict
from aux_functions import string_on_extracted_data
from aux_functions import check_email_reg_exp
from config import Config

# Initialize Flask Application
app = Flask(__name__)

# Default configurataion for the app
app.config['SQLALCHEMY_DATABASE_URI']        = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Enable/Disable debug
#app.config['SQLALCHEMY_ECHO'] = True

# Create API from this app
api = Api(app)

## CREATE ENGINE and SESSION using the declarative way
sqlalchemy_database_uri = app.config['SQLALCHEMY_DATABASE_URI']
engine                  = create_engine(sqlalchemy_database_uri,
                                        convert_unicode=True,
                                        echo=False)#'debug')#False)#'debug')
DBSession               = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db_session              = scoped_session(DBSession)

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

##########################
# INITIALIZING DATA BASE #
##########################
@app.before_first_request
def setup():
    print("debug: setup app")
    # Drop all tables 
    if Config.DROP_ALL_TABLES_ON_START:
        Base.metadata.drop_all(bind=engine)
        
    # Binding Base Model class to the engine
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

###############################
# DEFINING API REPRESENTATION #
###############################
@api.representation('application/json')
def jsonify_output(data, status_code=200, headers=None, indent=4):
    print("debug: outputting in json format with status code "+str(status_code))
    try:
        resp = make_response(json.dumps(data,indent=indent), status_code)
    except Exception:
        print("debug: Error creating response")
        abort(500)

    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['mimetype'] = 'application/json'
    resp.status_code = status_code
    return resp

###########################
# DEFINING ERROR HANDLERS #
###########################
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify_output({"status":405,
                           "message":Config.MSG_HTTP_INVALID},405)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify_output({"status":404,
                           "message":Config.MSG_RESOURCE_NOT_FOUND},404)    
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify_output({"status":500,
                           "message":Config.MSG_INTERNAL_ERROR},500)    
                          
@app.errorhandler(Exception) 
def handle_error(error):
    print("debug: handle_error")
    if isinstance(error,werkzeug.exceptions.MethodNotAllowed):
        return jsonify_output({"status":405,
                               "message":Config.MSG_HTTP_INVALID},405)

    if isinstance(error,werkzeug.exceptions.NotFound):
        return jsonify_output({"status":404,
                               "message":Config.MSG_RESOURCE_NOT_FOUND},404)    

    if isinstance(error,sqlalchemy.exc.IntegrityError):
        return jsonify_output({"status":400,
                               "message":Config.MSG_INTEGRITY_ERROR},400)
    # Anything else
    return jsonify_output({"status":500,
                           "message":Config.MSG_INTERNAL_ERROR},500)    

######################
## SHUTTING DOWN APP #
######################
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#########################
# DEFINING FLASK ROUTES #
#########################
    
# This receives only POST method using json
@app.route('/contact/',methods=['POST'])
def post_contact():
    print("debug: post_contact")
    
    mydict={}
    try:
        ''' This function is only used from POST and PUT routes
        This shoud try to parse JSON content from request data
        otherwise return non JSON format '''
        mydict = request.get_json()  
    except:
        data,status = output_bad_request(Config.MSG_BAD_DATA_FORMAT)
        return jsonify_output(data,status)

    if mydict == {}:
        data,status = output_bad_request(Config.MSG_VOID_DATA_JSON)
        return jsonify_output(data,status)
    
    extractData = get_data_from_dict(mydict)

    isBadData,message = string_on_extracted_data(extractData)    
    if isBadData:
        data,status = output_bad_request(message)
        return jsonify_output(data,status)

    username = extractData[0]    
    new_contact = Contact(username,
                          extractData[1],
                          extractData[2],
                          extractData[3])

    # Append list emails on its table
    for email in extractData[1].split("|"):
        new_email = Email(username,email)
        db_session.add(new_email)

    # Add new contact to db
    db_session.add(new_contact)
    db_session.commit()

    # Return OK message
    message = Config.MSG_OK_CONTACT_INSERT+" ( Username = "+username+" )"
    status  = 200
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
            contactDict=query.toDict()
            contactDict["email"] = contactDict["email"].split("|")        
            listOfContacts.append(contactDict)
        status = 200 
        data = {"status":status,
                "message":Config.MSG_OK_ALL_CONTACT_RET,
                "contacts":listOfContacts}     
        return jsonify_output(data, status)    
    else:
        abort(404)
    
@app.route('/contact/<username>',methods=['GET']) 
def get_single_contact(username):
    print('debug: get_single_contact')
    # Querying contact matching username    
    myQueryContact = Contact.query.filter(Contact.username == username).first()    
    if myQueryContact != None:
        contactDict = myQueryContact.toDict()        
        contactDict["email"] = contactDict["email"].split("|")
        status = 200
        data = {"status":status,
                "message":Config.MSG_OK_CONTACT_RET,
                "contact":contactDict}     
        
        return jsonify_output(data, status)
    else:
        data,status = output_not_found(username)
        return jsonify_output(data, status)

@app.route('/contact/email/<email>',methods=['GET']) 
def get_contacts_by_email(email):
    print('debug: get_contacts_by_email')
    # Check that input email is a valid one
    if not check_email_reg_exp(email):
        status = 400
        data = {"status":status,
                "message":Config.MSG_INVALID_EMAIL}
        return jsonify_output(data, status)
        
    # Querying usernames by incoming emails
    myQueryEmails = Email.query.filter(Email.email == email).all()


    if myQueryEmails == []:
        message = Config.MSG_DATA_NOT_FOUND
        status = 404
        data = {"status":status,
                "message":message}
        return jsonify_output(data,status)

        
    listContactsWithEmail=[]
    for queryEmail in myQueryEmails:
        username = queryEmail.username

        myQueryContact = Contact.query.filter(Contact.username == username).first()
        myDictQueryContact = myQueryContact.toDict()
        myDictQueryContact["email"] = myDictQueryContact["email"].split('|')
        listContactsWithEmail.append(myDictQueryContact)
        
    message = Config.MSG_OK_CONTACT_BY_EMAIL
    status = 201
    data = {"status":status,
            "message":message,
            "email":email,
            "contacts":listContactsWithEmail}
        
    return jsonify_output(data,status)
    
    
@app.route('/contact/<username>',methods=['PUT'])
def update_single_contact(username):
    print("debug: updating single contact")
    myQueryContact = Contact.query.filter(Contact.username == username).first()    
    if myQueryContact != None:
        mydict={}
        try:
            ''' This function is only used from POST and PUT routes
            This shoud try to parser JSON content from request data
            otherwise return non JSON format '''
            mydict = request.get_json()
            mydict['username'] = username
        except:
            data,status = output_bad_request(Config.MSG_BAD_DATA_FORMAT)
            return jsonify_output(data, status)
        
        extractData = get_data_from_dict(mydict)
        isBadData,message = string_on_extracted_data(extractData)

        if isBadData:
            data,status = output_bad_request(message)
            return jsonify_output(data, status)
                
        myQueryContact.email     = extractData[1]
        myQueryContact.firstname = extractData[2]
        myQueryContact.surname   = extractData[3]

        # Delete previous Emails on its table by username
        # Notice that at least one email must exist since email in contact is not null
        myQueryEmails = Email.query.filter(Email.username == username)
        myQueryEmails.delete()
        
        # Append list of input emails (validated) into the Email table
        for email in extractData[1].split("|"):
            username  = extractData[0]
            new_email = Email(username,email)
            db_session.add(new_email)

        # Commit changes
        db_session.commit()

        message = Config.MSG_OK_CONTACT_UPDATED
        status = 201
        data = {"message":message,"status":status,
                "contact_updated":{"username":username,
                                   "email":myQueryContact.email.split("|"),
                                   "firstname":myQueryContact.firstname,
                                   "surname":myQueryContact.surname}}
        
        return jsonify_output(data,status)
    else:
        data,status = output_not_found(username)
        return jsonify_output(data,status)


@app.route('/contact/<username>',methods=['DELETE'])
def delete_single_contact(username):
    print("debug: Deleting single contact")
    queryContact = Contact.query.filter(Contact.username == username).first()
    if queryContact != None:

        queryContact = Contact.query.filter(Contact.username == username)
        queryContact.delete()
        db_session.commit()

        message = Config.MSG_DEL_CONTACT
        status = 200
        data = {"message":message,"status":status}
        return jsonify_output(data,status)
    else:
        data,status = output_not_found(username)    
        return jsonify_output(data,status)















