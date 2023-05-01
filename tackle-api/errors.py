import traceback

from sqlalchemy import exc
from marshmallow.exceptions import MarshmallowError


"""
The exceptions defined in this module are wrappers of the following types of errors:
    Middleware Errors:
        SqlException: Either a sqlalchemy exception or a sqlite3 exception (details are stored in the error message)
        SerializationException: A marshmallow exception when serializing the data as JSON
    Runtime Errors:
        DataNotFoundException: The requested resource was not found
        InvalidInputException: The input data is invalid
"""
class DataNotFoundException(RuntimeError):
    def __init__(self, id, resource_type):
        super().__init__(f"ID '{id}' not found.")
        self.resource_type = resource_type
        
class SqlException(exc.SQLAlchemyError):
    def __init__(self, error, resource_type):
        super().__init__(error)
        self.resource_type = resource_type
        
        
class InvalidInputException(ValueError):
    def __init__(self, error, resource_type):
        super().__init__(error)
        self.resource_type = resource_type
        
        
class SerializationException(MarshmallowError):
    def __init__(self, error, resource_type):
        super().__init__(error)
        self.resource_type = resource_type


"""
Handlers are defined in this module and bound to the Flask application.
They return a JSON response with the appropriate status code, error message, and the relevant resource type.
"""

        
def not_found_handler(error):
    return {
        "detail": str(error),
        "status": 404,
        "resource_type": error.resource_type,
    }, 404
    

def sql_exception_handler(error):
    return {
        "detail": error.__repr__(),
        "status": 500,
        "resource_type": error.resource_type,
    }, 500
    
    
def invalid_input_handler(error):
    return {
        "detail": traceback.format_exception(type(error), error, error.__traceback__),
        "status": 405,
        "resource_type": error.resource_type,
    }, 405
    
    
def serialization_exception_handler(error):
    return {
        "detail": traceback.format_exception(type(error), error, error.__traceback__),
        "status": 500,
        "resource_type": error.resource_type,
    }, 500