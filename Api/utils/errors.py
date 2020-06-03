class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class BlogDoesNotExist(Exception):
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
    }
}