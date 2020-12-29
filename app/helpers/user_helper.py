from ..extensions import db
from ..models import User, Fund
from .api_error_helper import APIException


class UserHelper:
    @staticmethod
    def save_new_user(data):
        try:
            user = User.query.filter_by(
                username=data['username'].lower()).first()
            if not user:
                new_user = User(
                    username=data['username'].lower(),
                    name=data['name'].title()
                )
                db.session.add(new_user)
                db.session.commit()
                new_fund = Fund(
                    total_amount=50000,
                    invested_amount=50000,
                    user_id=new_user.id
                )
                db.session.add(new_fund)
                db.session.commit()
                return True
            else:
                return None
        except Exception as e:
            print(e)
            raise APIException
