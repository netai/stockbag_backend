import datetime
from ..extensions import db
from ..models import Note
from .api_error_helper import APIException


class NoteHelper:
    @staticmethod
    def save_new_note(data):
        try:
            if data['note'] and data['holding_id']:
                note = Note(
                    text=data['note'],
                    holding_id=data['holding_id']
                )
                db.session.add(note)
                db.session.commit()
            return True
        except Exception as e:
            print(e)
            raise APIException

    @staticmethod
    def get_holding_notes(holding_id=None):
        """return holding notes"""
        try:
            notes = Note.query.filter_by(holding_id=holding_id).all()
            return notes
        except Exception as e:
            raise APIException

    @staticmethod
    def delete_note(id=None):
        try:
            Note.query.filter_by(id=id).delete()
            db.session.commit()
        except Exception as e:
            raise APIException
