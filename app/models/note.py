import datetime
from ..extensions import db

class Note(db.Model):
    """Note model for storing Note retated details"""
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    important = db.Column(db.Boolean, nullable=False, default=False)
    holding_id = db.Column(db.Integer, db.ForeignKey('holding.id'))
    note_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Note 'id: {}, type: {}'>".format(self.id,self.text)