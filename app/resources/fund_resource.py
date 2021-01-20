from flask_restful import Resource, reqparse
from ..helpers import FundHelper, APIException, InsufficientFundException
from ..util.decorator import token_required


class Fund(Resource):
    @token_required
    def get(self):
        """get fund detail"""
        try:
            fund_data = FundHelper.get_fund_detail()
            if fund_data:
                resp_obj = {
                    'status': 'success',
                    'data': {
                        'fund': fund_data
                    }
                }
                return resp_obj, 200
            else:
                raise APIException
        except APIException as e:
            return e.data

    @token_required
    def put(self):
        """save fund detail"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('amount', type=float, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('req_type', type=str, required=True,
                                help='This field cannot be left blank')
            args = parser.parse_args()
            rtn = FundHelper.add_withdraw(data=args)
            if rtn == 'success':
                resp_obj = {
                    'status': 'success',
                    'message': 'Fund successfully added/withdraw.'
                }
            elif rtn == 'insufficient_fund':
                raise InsufficientFundException
            return resp_obj, 200
        except APIException as e:
            return e.data
