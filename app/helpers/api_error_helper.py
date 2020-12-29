class APIException(Exception):
    code = 500
    message = "Something went wrong, Please try after sometime."

    @property
    def data(self):
        return {'status': 'failure', 'message': self.message}, self.code


class ResourceNotExistException(APIException):
    code = 200
    message = "Requested resource not found."


class UnauthorizedException(APIException):
    code = 401
    message = "Invalid username/password."


class ResourceExistException(APIException):
    code = 200
    message = "Requested resource already exists."


class InvalidAuthTokenException(APIException):
    code = 401
    message = "Provide a valid auth token."

class InsufficientFundException(APIException):
    code = 200
    message = "Insufficient fund."
