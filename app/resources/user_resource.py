from flask_restful import Resource, reqparse
from ..helpers import UserHelper, APIException, ResourceExistException


class User(Resource):
    def post(self):
        """Creates a new User """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('username', type=str, required=True,
                                help='This field cannot be left blank')
            args = parser.parse_args()
            if UserHelper.save_new_user(data=args):
                resp_obj = {
                    'status': 'success',
                    'message': 'User successfully created.'
                }
            else:
                raise ResourceExistException
            return resp_obj, 200
        except APIException as e:
            return e.data
