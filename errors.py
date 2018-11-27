from flask import abort

'''
Code 	Status 	          Field 	Description
401 	NOT_AUTHORIZED 	  null   	Invalid token or user not authenticated
400 	INVALID_FIELD 	  “field_name” 	Missing or invalid field
400 	INVALID_SERVICE   null 	        Service ID mentioned in path does not belong to said Event
404 	NOT_FOUND 	  null 	        Event or Service not found
405     METHOD NOT ALLOWED null         HTTP Method not allowed for request
403 	PERMISSION_DENIED null 	        User role not allowed to perform such action
500 	SERVER_ERROR 	  null  	Internal server error
'''

class BaseError(Exception):
    """Base Error Class"""

    def __init__(self, code=400, message='', status='', field=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.status = status
        self.field = field

    def to_dict(self):
        return {'code': self.code,
                'message': self.message,
                'status': self.status,
                'field': self.field, }

class NotFoundError(BaseError):
    def __init__(self, message='Not found'):
        BaseError.__init__(self)
        self.code = 404
        self.message = message
        self.status = 'NOT_FOUND'

class NotAuthorizedError(BaseError):
    def __init__(self, message='Unauthorized'):
        BaseError.__init__(self)
        self.code = 401
        self.message = message
        self.status = 'NOT_AUTHORIZED'

class ValidationError(BaseError):
    def __init__(self, field, message='Invalid field'):
        BaseError.__init__(self)
        self.code = 400
        self.message = message
        self.status = 'INVALID_FIELD'
        self.field = field

class InvalidServiceError(BaseError):
    def __init__(self, message='Internal server error'):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = 'SERVER_ERROR'


class MethodNotAllowed(BaseError):
    def __init__(self, message='HTTP Method not Allowed for this request'):
        BaseError.__init__(self)
        self.code = 405
        self.message = message
        self.status = 'SERVER_ERROR'
    
