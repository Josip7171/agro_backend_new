import mysql.connector
from flask_restful import Resource, reqparse

mysql_config = {
    'user': 'root',
    'password': 'sifra321',
    'host': '127.0.0.1',
    'database': 'agro2',
    'raise_on_warnings': True
}


class Note:
    def __init__(self, _id, user_id, content):
        self.id = _id
        self.user_id = user_id
        self.content = content

    @classmethod
    def find_by_userid(cls, user_id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM notes WHERE user_id=%s"
        result = cursor.execute(query, (user_id,))     # mozda se moze "result" negdje iskoristit..
        # drugi parameter za cursor.execute uvijek mora biti u tuple!
        row = cursor.fetchall()
        if row:
            notes = cls(*row)
        else:
            notes = None

        connection.close()
        return notes


class CreateNote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'content',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    def post(self):
        data = CreateNote.parser.parse_args()

        if Note.find_by_userid(data['user_id']) is False:
            return {"message": "User with that ID does not exist."}, 400

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "INSERT INTO notes VALUES (NULL, %s, %s)"
        cursor.execute(query, (data['user_id'], data['content']))

        connection.commit()
        connection.close()

        return {'message': "note created successfully"}, 201
