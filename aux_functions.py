
from config import Config

# Not Found message configured
def output_not_found(username):
    print("debug: output_not_found")
    message = Config.MSG_DATA_NOT_FOUND+" Username '"+username+ \
              "' does not exist."
    status = 404
    data = {"status":status,"message":message}
    return data,status

def output_bad_request(message):
    print("debug: output_bad_request")
    status = 400
    message = Config.MSG_BAD_REQUEST+" "+message
    data = {"status":status,"message":message}
    return data,status

def check_email_reg_exp(email):
    print("debug: check email reg exp")
    ''' Check whether email follows a regular expression'''
    import re
    # If email is passed check regular expresion
    regexp=Config.REGEXP_EMAIL
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
        return Config.INVALID_KEYS

    username  = mydict['username']
    if username == None:
        return Config.NULL_KEY_ID

    email     = mydict['email']                
    if not check_email_reg_exp(email):
        return Config.INVALID_EMAIL

    firstname = mydict['firstname']
    surname   = mydict['surname']

    # Create tuple with the inputs to update or insert a new contact
    return (username,email,firstname,surname)

      
def string_on_extracted_data(extractData):
    ''' Determine whether extracted data is good or bad'''
    print("debug: check extracted data")

    if isinstance(extractData,str):
        print("debug: Extracted data is wrong")
        msg = Config.BAD_DATA
        if extractData == Config.INVALID_USERNAME:
            msg = Config.MSG_INVALID_USERNAME

        if extractData == Config.INVALID_KEYS:
            msg = Config.MSG_INVALID_KEYS 
        if extractData == Config.NULL_KEY_ID:
            msg = Config.MSG_NULL_KEY_ID
        if extractData == Config.INVALID_EMAIL:
            msg = Config.MSG_INVALID_EMAIL


        return (True,msg)
    else:

        return (False,"OK")
