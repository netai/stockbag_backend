import datetime
from flask import g
from ..extensions import db
from ..models import Fund, Holding
from .api_error_helper import APIException


class FundHelper:
    @staticmethod
    def add_fund(data):
        try:
            user_id = g.user['id']
            fund = Fund.query.filter_by(user_id=user_id).first()
            if fund and data['amount']:
                fund.invested_amount += data['amount']
                fund.total_amount += data['amount']
                db.session.add(fund)
                db.session.commit()
                return True
            else:
                return None
        except Exception as e:
            raise APIException

    @staticmethod
    def add_withdraw(data):
        try:
            user_id = g.user['id']
            fund = Fund.query.filter_by(user_id=user_id).first()
            if fund and data['amount']:
                unreleased_amount = 0
                holding = Holding.query.filter_by(user_id=user_id).all()
                if holding:
                    for row in holding:
                        unreleased_amount += row.avg_price * row.qty
                profit_amount = (fund.total_amount +
                                 unreleased_amount)-fund.invested_amount
                if data['req_type'] == 'add':
                    fund.invested_amount += data['amount']
                    fund.total_amount += data['amount']
                elif data['req_type'] == 'withdraw':
                    if fund.total_amount >= data['amount']:
                        fund.total_amount -= data['amount']
                        if profit_amount < data['amount']:
                            fund.invested_amount -= (
                                data['amount'] - profit_amount)
                    else:
                        return 'insufficient_fund'
                db.session.add(fund)
                db.session.commit()
            return 'success'
        except Exception as e:
            raise APIException

    @staticmethod
    def get_fund_detail():
        try:
            user_id = g.user['id']
            fund = Fund.query.filter_by(user_id=user_id).first()
            holding = Holding.query.filter_by(user_id=user_id).all()
            unreleased_amount = 0
            total_amount = 0
            invested_amount = 0
            if holding:
                for row in holding:
                    unreleased_amount += row.avg_price * row.qty
            if fund:
                total_amount = fund.total_amount
                invested_amount = fund.invested_amount
            return {
                'total_amount': total_amount,
                'invested_amount': invested_amount,
                'unreleased_amount': unreleased_amount
            }
        except Exception as e:
            raise APIException
