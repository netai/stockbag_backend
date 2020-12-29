from ..models import User
from .api_error_helper import APIException


class AuthHelper:
    @staticmethod
    def auth_user(data):
        try:
            user = User.query.filter_by(
                username=data['username'].lower()).first()
            if user:
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    data = {
                        'token': auth_token.decode(),
                        'user': {
                            'name': user.name,
                            'mobile': (user.mobile or ''),
                            'admin': user.admin,
                            'username': user.username,
                        }
                    }
                    return data
            else:
                return None
        except Exception as e:
            raise APIException

    @staticmethod
    def get_user_by_token(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp:
                user = User.query.filter_by(id=resp).first()
                if user:
                    response_object = {
                        'id': user.id,
                        'name': user.name,
                        'username': user.username,
                        'admin': user.admin
                    }
                    return response_object
                else:
                    return None
            else:
                return None
        else:
            return None
