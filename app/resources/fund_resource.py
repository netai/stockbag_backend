from flask_restful import Resource, reqparse
from ..helpers import FundHelper, APIException, ResourceNotExistException
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
