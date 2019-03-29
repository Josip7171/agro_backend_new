import mysql.connector
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
    def get(self, user_id):
        try:
            note = self.find_by_userid(user_id)
        except:
            return {'message': 'User not found.'}

        if note:
            return note
        return {'message': 'Note not found.'}

    @classmethod
    def find_by_userid(cls, user_id):       # ova metoda nađe SVE bilješke iz tablice "notes"
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

        connection.commit()
        connection.close()
        return {'notes': notes}

    # @jwt_required()
    def post(self, user_id):
        data = Note.parser.parse_args()

        note = {
            'user_id': user_id,
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


class SingleNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'content',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, id):
        try:
            note = self.find_by_id(id)
        except:
            return {'message': 'Note not found.'}, 500
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

    def delete(self, id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "DELETE FROM notes WHERE id=%s"
        result = cursor.execute(query, (id,))

        connection.commit()
        connection.close()
        return {'message': 'Note successfully deleted.'}

    def put(self, id):
        data = SingleNote.parser.parse_args()

        note = self.find_by_id(id)
        updated_note = {
            'id': id,
            'user_id': data['user_id'],
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









