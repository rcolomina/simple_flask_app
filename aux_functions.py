
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
    print("debug: checking email regular expression on "+email)
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

    # Here extract multiple emails (one or more)
    list_emails  = mydict['email']

    # Check whether email content is a list
    # e.g.:  ['jonhsmith@gmail.com','jonhsmith@hotmail.com','jsmiths@ibm.com']
    # Convert list into string "email1|email2|...|emailn"
    # Check emails are correct accross them

    # Check that emails come in a list
    if not isinstance(list_emails,list):
        #Check whether is a single string
        if not isinstance(list_emails,str):                
            return Config.INVALID_EMAIL
        else:
            if not check_email_reg_exp(list_emails):
                return Config.INVALID_EMAIL

            
    else:


        for email in list_emails:
            if not isinstance(email,str):        
                return Config.INVALID_EMAIL
            if not check_email_reg_exp(email):
                return Config.INVALID_EMAIL

        list_emails = "|".join(list_emails)
        
    firstname = mydict['firstname']
    surname   = mydict['surname']

    # Create tuple with the inputs to update or insert a new contact
    return (username,list_emails,firstname,surname)

      
def string_on_extracted_data(extractData):
    ''' Determine whether extracted data is good or bad'''
    print("debug: string_on_extracted_data")

    if isinstance(extractData,str):

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


