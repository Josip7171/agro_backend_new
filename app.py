from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, current_identity, jwt_required
from datetime import timedelta

from security import authenticate, identity
from user import UserRegister
from notes import Note, Notes
from weather import Weather


app = Flask(__name__)
app.secret_key = 'agro'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app)
jwt = JWT(app, authenticate, identity)          # stvori endpoint -> /auth


@app.route('/')
def hello_world():
    return 'Hi World!'


# testna ruta koja dohvaća ID vlasnika prosljeđenog JWT tokena
@app.route('/protected')
@jwt_required()
def protected():
    x = getattr(current_identity, 'id')     # x postaje ID usera čiji je token prosljeđen u auth header
    print("ja printam: {}".format(x))
    return '%s' % current_identity


api.add_resource(UserRegister, '/register')     # stvori endpoint -> /register
api.add_resource(Notes, '/notes/<int:user_id>')
api.add_resource(Note, '/note/<int:id>')
api.add_resource(Weather, '/weather/<string:city_name>')


if __name__ == '__main__':
    app.run()
