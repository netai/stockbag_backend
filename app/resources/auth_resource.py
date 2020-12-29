from flask_restful import Resource, reqparse
from ..helpers import AuthHelper, APIException, UnauthorizedException

class Login(Resource):
    """
        User Login Resource
    """

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
            args = parser.parse_args()
            resp_obj = {
                'status': '',
                'data': {}
            }
            user_data = AuthHelper.auth_user(data=args)
            if user_data:
                resp_obj['data'] = user_data
                resp_obj['status'] = 'success'
            else:
                raise UnauthorizedException
            return resp_obj, 200
        except APIException as e:
            return e.data
