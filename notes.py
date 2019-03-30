import mysql.connector
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity


mysql_config = {
    'user': 'root',
    'password': 'sifra321',
    'host': '127.0.0.1',
    'database': 'agro2',
    'raise_on_warnings': True
}


class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'content',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def post(self, id):
        curr_user_id = getattr(current_identity, 'id')

        data = Note.parser.parse_args()
        note = {
            'user_id': curr_user_id,
            'content': data['content']
        }

        try:
            self.insert(note)
        except:
            return {'message': 'An error occured inserting a note.'}, 500

        return note, 201

    @classmethod
    def insert(cls, note):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "INSERT INTO notes VALUES (NULL, %s, %s)"
        result = cursor.execute(query, (note['user_id'], note['content']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, id):
        try:
            note = self.find_by_id(id)
        except:
            return {'message': 'Note not found.'}, 500

        curr_user_id = getattr(current_identity, 'id')
        if note['note']['user_id'] != curr_user_id:
            return {'message': 'You are not authorized to do that.'}

        if note:
            return note
        return {'message': 'Note not found.'}, 404

    def find_by_id(cls, id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM notes WHERE id=%s"
        result = cursor.execute(query, (id,))
        row = cursor.fetchone()

        connection.close()
        if row:
            return {
                'note': {
                    'id': id,
                    'user_id': row[1],
                    'content': row[2]
                }
            }

    @jwt_required()
    def delete(self, id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT user_id FROM notes WHERE id=%s"
        result = cursor.execute(query, (id,))
        user_id = cursor.fetchone()

        curr_user_id = getattr(current_identity, 'id')
        if user_id[0] != curr_user_id:
            return {'message': 'You are not authorized to do that.'}

        query = "DELETE FROM notes WHERE id=%s"
        result = cursor.execute(query, (id,))

        connection.commit()
        connection.close()
        return {'message': 'Note successfully deleted.'}

    @jwt_required()
    def put(self, id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT user_id FROM notes WHERE id=%s"
        result = cursor.execute(query, (id,))
        user_id = cursor.fetchone()

        curr_user_id = getattr(current_identity, 'id')
        if user_id[0] != curr_user_id:
            return {'message': 'You are not authorized to do that.'}

        data = Note.parser.parse_args()

        updated_note = {
            'id': id,
            'content': data['content']
        }

        try:
            self.update(updated_note)
            return updated_note
        except:
            return {'message': 'An error occured updating the note.'}, 500

    @classmethod
    def update(cls, note):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "UPDATE notes SET content=%s WHERE id=%s"
        result = cursor.execute(query, (note['content'], note['id']))

        connection.commit()
        connection.close()


class Notes(Resource):
    @jwt_required()
    def get(self, user_id):
        curr_user_id = getattr(current_identity, 'id')
        if user_id != curr_user_id:
            return {'message': 'You are not authorized to do that.'}

        try:
            notes = self.find_by_userid(user_id)
        except:
            return {'message': 'User not found.'}

        if notes:
            return notes
        return {'message': 'Notes not found.'}

    @classmethod
    def find_by_userid(cls, user_id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM notes WHERE user_id=%s"
        result = cursor.execute(query, (user_id,))

        notes = []
        for row in cursor:
            notes.append({
                'id': row[0],
                'user_id': row[1],
                'content': row[2]
            })

        connection.close()
        return {'notes': notes}











