from functools import wraps
from flask import request, g
from ..helpers import AuthHelper, APIException, InvalidAuthTokenException


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = AuthHelper.get_user_by_token(request)
            if not data:
                raise InvalidAuthTokenException
            else:
                g.user = data
            return f(*args, **kwargs)
        except APIException as e:
            return e.data
    return decorated
