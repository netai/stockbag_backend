import datetime
from ..extensions import db

class Fund(db.Model):
    """Fund model for storing Fund retated details"""
    __tablename__ = "fund"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_amount = db.Column(db.Float, nullable=False, default=0)
    invested_amount = db.Column(db.Float, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Fund 'id: {}, type: {}'>".format(self.id,self.total_amount)