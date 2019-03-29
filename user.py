import mysql.connector
from flask_restful import Resource, reqparse

mysql_config = {
    'user': 'root',
    'password': 'sifra321',
    'host': '127.0.0.1',
    'database': 'agro2',
    'raise_on_warnings': True
}


class User:
    def __init__(self, _id, username, email, password, role):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    @classmethod
    def find_by_username(cls, username):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=%s"
        result = cursor.execute(query, (username,))
        # drugi parameter za cursor.execute uvijek mora biti u tuple!
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=%s"
        result = cursor.execute(query, (_id,))      # mozda se moze "result" negdje iskoristit..
        # drugi parameter za cursor.execute uvijek mora biti u tuple!
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'role',
        type=str,
        required=False,
        default='user'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, %s, %s, %s, %s)"
        cursor.execute(query, (data['username'], data['email'], data['password'], data['role']))

        connection.commit()
        connection.close()

        return {'message': "user created successfully"}, 201
