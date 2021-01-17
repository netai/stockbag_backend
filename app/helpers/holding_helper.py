from flask import g
import datetime
from ..extensions import db
from ..models import Holding, Script, Note, Fund
from .api_error_helper import APIException, InsufficientFundException, ResourceExistException
from .note_helper import NoteHelper


class HoldingHelper:
    @staticmethod
    def save_new_holding(data):
        try:
            user_id = g.user['id']
            script = Script.query.filter_by(symbol=data['symbol'].upper()).filter_by(
                exchange=data['exchange'].upper()).first()
            fund = Fund.query.filter_by(user_id=user_id).first()
            total_price = data['avg_price'] * data['qty']
            if fund.total_amount >= total_price:
                if not script:
                    script = Script(
                        symbol=data['symbol'].upper(),
                        exchange=data['exchange'].upper()
                    )
                    db.session.add(script)
                    db.session.commit()
                holding = Holding.query.filter_by(script_id=script.id).filter_by(
                    holding_type=data['holding_type'].lower()).filter_by(user_id=user_id).first()
                if not holding:
                    new_holding = Holding(
                        avg_price=data['avg_price'],
                        target_price=data['target_price'],
                        qty=data['qty'],
                        period=data['period'].upper(),
                        est_exit_date=datetime.datetime.strptime(
                            data['est_exit_date'], '%Y-%m-%d'),
                        holding_type=data['holding_type'].lower(),
                        script_id=script.id,
                        user_id=user_id,
                    )
                    db.session.add(new_holding)

                    # calculate fund
                    fund.total_amount -= total_price
                    db.session.add(fund)

                    db.session.commit()

                    data['holding_id'] = new_holding.id
                    NoteHelper.save_new_note(data)

                    return 'done'
                else:
                    raise 'is_exist'
            else:
                return 'insufficient_fund'
        except Exception as e:
            raise APIException

    @staticmethod
    def edit_holding(data):
        try:
            user_id = g.user['id']
            holding = Holding.query.filter_by(id=data['id']).first()
            if holding:
                fund = Fund.query.filter_by(user_id=user_id).first()
                new_total_price = data['avg_price'] * data['qty']
                old_total_price = holding.avg_price * holding.qty
                fund.total_amount += old_total_price
                if fund.total_amount >= new_total_price:
                    script = Script.query.filter_by(symbol=data['symbol'].upper()).filter_by(
                        exchange=data['exchange'].upper()).first()
                    if not script:
                        script = Script(
                            symbol=data['symbol'].upper(),
                            exchange=data['exchange'].upper()
                        )
                        db.session.add(script)
                        db.session.commit()

                    holding.avg_price = data['avg_price']
                    holding.target_price = data['target_price']
                    holding.qty = data['qty']
                    holding.period = data['period'].upper()
                    holding.est_exit_date = datetime.datetime.strptime(
                        data['est_exit_date'], '%Y-%m-%d')
                    holding.holding_type = data['holding_type'].lower()
                    holding.script_id = script.id

                    db.session.add(holding)
                    # calculate fund
                    fund.total_amount -= new_total_price
                    db.session.add(fund)
                    db.session.commit()

                    data['holding_id'] = holding.id
                    NoteHelper.save_new_note(data)

                    return 'done'
                else:
                    return 'insufficient_fund'
            else:
                return 'not_exist'
        except Exception as e:
            raise APIException

    @staticmethod
    def delete_holding(id):
        try:
            user_id = g.user['id']
            fund = Fund.query.filter_by(user_id=user_id).first()
            holding = Holding.query.filter_by(id=id).first()
            total_amount = 0
            if holding:
                total_amount = holding.avg_price * holding.qty
            Note.query.filter_by(holding_id=id).delete()
            Holding.query.filter_by(id=id).delete()
            # calculate fund
            fund.total_amount += total_amount
            db.session.add(fund)
            db.session.commit()
        except Exception as e:
            raise APIException

    @staticmethod
    def get_holding_all():
        """return holding list"""
        try:
            user_id = g.user['id']
            holding_list = db.session.query(Holding, Script).join(Script, Script.id == Holding.script_id)\
                .filter(Holding.user_id == user_id).order_by(Holding.holding_on.desc())
            return holding_list
        except Exception as e:
            raise APIException

    @staticmethod
    def get_holding_by_id(id=None):
        """return holding list"""
        try:
            user_id = g.user['id']
            holding = db.session.query(Holding, Script).join(Script, Script.id == Holding.script_id)\
                .filter(Holding.id == id).first()
            return holding
        except Exception as e:
            raise APIException

    @staticmethod
    def add_exit_holding(data):
        try:
            user_id = g.user['id']
            holding = Holding.query.filter_by(id=data['id']).first()
            if holding:
                fund = Fund.query.filter_by(user_id=user_id).first()
                total_amount = data['avg_price'] * data['qty']
                if data['req_type'] == 'add' and fund.total_amount < total_amount:
                    return 'insufficient_fund'
                else:
                    additional_note = "<b>{} (Price: {}, Quantity: {})</b>".format(
                    data['req_type'].upper(), data['avg_price'], data['qty'])
                    if data['req_type'] == 'add':
                        total_price = (holding.avg_price * holding.qty) + \
                            (data['avg_price'] * data['qty'])
                        total_qty = holding.qty + data['qty']
                        holding.avg_price = round((total_price/total_qty), 2)
                        holding.qty = total_qty
                        fund.total_amount -= total_amount
                    else:
                        holding.qty = (holding.qty - data['qty'])
                        fund.total_amount += total_amount

                    if holding.qty > 0:
                        if data['note']:
                            additional_note += ' - ' + data['note']
                        NoteHelper.save_new_note({
                            'note': additional_note,
                            'holding_id': data['id']
                        })
                        db.session.add(holding)
                    else:
                        Note.query.filter_by(
                            holding_id=data['id']).delete()
                        Holding.query.filter_by(id=data['id']).delete()

                    db.session.add(fund)
                    db.session.commit()
                    db.session.commit()
                    return 'done'
            else:
                return 'not_exist'
        except Exception as e:
            raise APIException
