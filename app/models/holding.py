import datetime
from ..extensions import db

class Holding(db.Model):
    """Holding model for storing holding retated details"""
    __tablename__ = "holding"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avg_price = db.Column(db.Float, nullable=False, default=0)
    target_price = db.Column(db.Float, nullable=False, default=0)
    qty = db.Column(db.Integer, nullable=False, default=0)
    # S-short(7 days), M-medium(30 days), L-long(365 days)
    period = db.Column(db.String(1), nullable=False, default='S')
    est_exit_date = db.Column(db.DateTime, nullable=False)
    holding_type = db.Column(db.String(5), nullable=False, default='buy')
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    holding_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Holding 'id: {}, type: {}'>".format(self.id,self.holding_type)