import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):    
    # SqlAlchemy Configuration 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'myapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_ENGINE_DEBUG_ON             = True
    DROP_ALL_TABLES_ON_START       = False  # WARNING!! True values may produce data loss.
    
    # Error Strings
    BAD_DATA             = "BAD_DATA"
    BAD_REQUEST          = "BAD_REQUEST"
    INVALID_USERNAME     = "INVALID_USERNAME"
    INVALID_KEYS         = "INVALID_KEYS"
    NULL_KEY_ID          = "NULL_KEY_ID"
    INVALID_EMAIL        = "INVALID_EMAIL"

    # Regular expresion to parse email
    REGEXP_EMAIL         = "^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

    # Returning message from request
    MSG_OK_ALL_CONTACT_RET = "All Contacts were retrieved succesfully from the database."
    MSG_OK_CONTACT_BY_EMAIL= "Contacts retrieved succesfully from the database by email"
    MSG_OK_CONTACT_RET     = "Specific Contact retrieved succesfully from the database."
    MSG_OK_CONTACT_INSERT  = "Contact inserted succesfully in the database."
    MSG_OK_CONTACT_UPDATED = "Contact updated  succesfully in the database."
    MSG_BAD_DATA_FORMAT    = "Data not provided in JSON format."
    MSG_BAD_REQUEST        = "Bad Request."
    MSG_VOID_DATA_JSON     = "A void Json file was provided in the request."
    MSG_DEL_CONTACT        = "Contact deleted from the database."
    MSG_HTTP_INVALID       = "HTTP Method was Not Allowed for the Request."
    MSG_RESOURCE_NOT_FOUND = "Resource Not Found or Not Available."
    MSG_INTERNAL_ERROR     = "Internal Server Error Found."
    MSG_INTEGRITY_ERROR    = "Integrity Error due to Duplicated Index or Null Key was provided."
    MSG_DATA_NOT_FOUND     = "Contant Not Found in database."
    MSG_INVALID_USERNAME   = "Username Primary Key Not provided in Data Body JSON request."
    MSG_INVALID_KEYS       = "Invalid Keys in Data JSON request."
    MSG_NULL_KEY_ID        = "Null Primary Key was provided in Data JSON request."            
    MSG_INVALID_EMAIL      = "Invalid email pattern found."
