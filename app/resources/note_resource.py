from flask_restful import Resource, reqparse
from ..helpers import NoteHelper, APIException, ResourceNotExistException
from ..util.decorator import token_required


class Note(Resource):
    @token_required
    def post(self, holding_id):
        """Creates a new note """
        try:
            if holding_id:
                parser = reqparse.RequestParser()
                parser.add_argument('note', type=str, required=True,
                                    help='This field cannot be left blank')
                args = parser.parse_args()
                args['holding_id'] = holding_id
                NoteHelper.save_new_note(data=args)
                resp_obj = {
                    'status': 'success',
                    'message': 'Note successfully saved.'
                }
                return resp_obj, 200
            else:
                raise ResourceNotExistException
        except APIException as e:
            return e.data

    @token_required
    def get(self, holding_id):
        """get note list"""
        try:
            if holding_id:
                note_list = []
                note_data = NoteHelper.get_holding_notes(holding_id)
                for row in note_data:
                    note_list.append({
                        'id': row.id,
                        'text': row.text,
                        'important': row.important,
                        'note_on': row.note_on.strftime("%Y-%m-%d %H:%M:%S")
                    })
                resp_obj = {
                    'status': 'success',
                    'data': {
                        'notes': note_list
                    }
                }
                return resp_obj, 200
            else:
                raise ResourceNotExistException
        except APIException as e:
            return e.data

    @token_required
    def delete(self, holding_id, id):
        """delete note """
        try:
            if holding_id and id:
                NoteHelper.delete_note(id)
                resp_obj = {
                    'status': 'success',
                    'message': 'Note successfully deleted.'
                }
                return resp_obj, 200
            else:
                raise ResourceNotExistException
        except APIException as e:
            return e.data
