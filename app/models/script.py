import datetime
from ..extensions import db

class Script(db.Model):
    """Script model for storing Script retated details"""
    __tablename__ = "script"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(100), nullable=False)
    exchange = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return "<Script 'id: {}, script: {}'>".format(self.id,self.script)