from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user2 import UserRegister
from notes import Note


app = Flask(__name__)
app.secret_key = 'agro'
api = Api(app)
jwt = JWT(app, authenticate, identity)          # stvori endpoint -> /auth


@app.route('/')
def hello_world():
    return 'Hi World!'


api.add_resource(UserRegister, '/register')     # stvori endpoint -> /register
api.add_resource(Note, '/notes/<int:user_id>')


if __name__ == '__main__':
    app.run()
