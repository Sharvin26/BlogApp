class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class BlogDoesNotExist(Exception):
    pass

class FieldAlreadyExistsError(Exception):
    pass

class PasswordValidationFailed(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class UserDoesnotExistsError(Exception):
    pass

class NotAllowed(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

class ExpiredTokenError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "BlogDoesNotExist": {
        "message": "Blog with given id doesn't exists",
        "status": 404
    },
    "FieldAlreadyExistsError": {
        "message": "Already exists",
        "status": 403
    },
    "PasswordValidationFailed": {
	    "message": "8 characters. Must contain [a-zA-z0-9]",
        "status": 400
    },
    "UnauthorizedError": {
	    "message": "Invalid email or password",
        "status": 401
    },
    "UserDoesnotExistsError": {
	    "message": "User does not exists",
	    "status": 404
    },
    "NotAllowed": {
        "message": "Not Allowed",
        "status": 403
    },
    "EmailAlreadyExistsError": {
        "message": "EmailAlreadyExistsError",
        "status": 409
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "ExpiredTokenError": {
        "message": "Token expired",
        "status": 404
    }
}