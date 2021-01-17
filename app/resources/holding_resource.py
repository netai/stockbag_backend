from flask_restful import Resource, reqparse
from ..helpers import HoldingHelper, APIException, ResourceExistException, ResourceNotExistException, InsufficientFundException
from ..util.decorator import token_required


class HoldingList(Resource):
    @token_required
    def get(self):
        """get holding list"""
        try:
            holding_list = []
            holding_data = HoldingHelper.get_holding_all()
            for row in holding_data:
                holding_list.append({
                    'id': row.Holding.id,
                    'symbol': row.Script.symbol,
                    'exchange': row.Script.exchange,
                    'avg_price': row.Holding.avg_price,
                    'target_price': row.Holding.target_price,
                    'qty': row.Holding.qty,
                    'period': row.Holding.period,
                    'est_exit_date': row.Holding.est_exit_date.strftime("%Y-%m-%d"),
                    'holding_type': row.Holding.holding_type,
                    'script_id': row.Holding.script_id,
                    'holding_on': row.Holding.holding_on.strftime("%Y-%m-%d %H:%M:%S"),
                })
            resp_obj = {
                'status': 'success',
                'data': {
                    'holding_list': holding_list
                }
            }
            return resp_obj, 200
        except APIException as e:
            return e.data


class Holding(Resource):
    @token_required
    def post(self):
        """Creates a new holding """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('symbol', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('exchange', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument(
                'avg_price', type=float, required=True, help='This field cannot be left blank')
            parser.add_argument('target_price', type=float,
                                required=True, help='This field cannot be left blank')
            parser.add_argument('qty', type=int, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('period', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument(
                'est_exit_date', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument(
                'holding_type', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('note', type=str)
            args = parser.parse_args()
            exe_status = HoldingHelper.save_new_holding(data=args)
            if exe_status=='done':
                resp_obj = {
                    'status': 'success',
                    'message': 'Holding successfully saved.'
                }
            elif exe_status=='insufficient_fund':
                raise InsufficientFundException
            else:
                raise ResourceExistException
            return resp_obj, 200
        except APIException as e:
            return e.data

    @token_required
    def get(self, id):
        """get holding list"""
        try:
            if id:
                holding_data = HoldingHelper.get_holding_by_id(id)
                holding = {
                    'id': holding_data.Holding.id,
                    'symbol': holding_data.Script.symbol,
                    'exchange': holding_data.Script.exchange,
                    'avg_price': holding_data.Holding.avg_price,
                    'target_price': holding_data.Holding.target_price,
                    'qty': holding_data.Holding.qty,
                    'period': holding_data.Holding.period,
                    'est_exit_date': holding_data.Holding.est_exit_date.strftime("%Y-%m-%d"),
                    'holding_type': holding_data.Holding.holding_type,
                    'script_id': holding_data.Holding.script_id,
                    'holding_on': holding_data.Holding.holding_on.strftime("%Y-%m-%d %H:%M:%S"),
                }
                resp_obj = {
                    'status': 'success',
                    'data': {
                        'holding': holding
                    }
                }
                return resp_obj, 200
            else:
                raise ResourceNotExistException
        except APIException as e:
            return e.data

    @token_required
    def put(self):
        """update holding """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('symbol', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('exchange', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument(
                'avg_price', type=float, required=True, help='This field cannot be left blank')
            parser.add_argument('target_price', type=float,
                                required=True, help='This field cannot be left blank')
            parser.add_argument('qty', type=int, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('period', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument(
                'est_exit_date', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument(
                'holding_type', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('note', type=str)
            parser.add_argument('id', type=int, required=True,
                                help='This field cannot be left blank')
            args = parser.parse_args()
            exe_status = HoldingHelper.edit_holding(data=args)
            if exe_status=='done':
                resp_obj = {
                    'status': 'success',
                    'message': 'Holding successfully updated.'
                }
            elif exe_status=='insufficient_fund':
                raise InsufficientFundException
            elif exe_status=='is_exist':
                raise ResourceExistException
            else:
                raise ResourceNotExistException
            return resp_obj, 200
        except APIException as e:
            return e.data

    @token_required
    def delete(self, id):
        """delete holding """
        try:
            if id:
                HoldingHelper.delete_holding(id)
                resp_obj = {
                    'status': 'success',
                    'message': 'Holding successfully deleted.'
                }
                return resp_obj, 200
            else:
                raise ResourceNotExistException
        except APIException as e:
            return e.data


class HoldingAddExit(Resource):
    @token_required
    def put(self):
        """add and exit holding """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'id', type=int, required=True, help='This field cannot be left blank')
            parser.add_argument(
                'avg_price', type=float, required=True, help='This field cannot be left blank')
            parser.add_argument('qty', type=int, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('req_type', type=str, required=True,
                                help='This field cannot be left blank')
            parser.add_argument('note', type=str)
            args = parser.parse_args()
            if HoldingHelper.add_exit_holding(data=args):
                resp_obj = {
                    'status': 'success',
                    'message': 'Holding successfully added/exit.'
                }
            else:
                raise ResourceNotExistException
            return resp_obj, 200
        except APIException as e:
            return e.data
