from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, current_identity, jwt_required
from datetime import timedelta

from security import authenticate, identity
from user import UserRegister
from notes import Note, Notes
from weather import Weather
from crop import Crops, Crop, CropData, CropEco, CropCult
from action_calendar import ActionCal, CropAction
from algorithms import MedianValues


app = Flask(__name__)
app.secret_key = 'agro'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app)
jwt = JWT(app, authenticate, identity)          # stvara endpoint -> /auth


@app.route('/')
def hello_world():
    return 'Hi World!'


# testna ruta koja dohvaća ID vlasnika prosljeđenog JWT tokena
@app.route('/protected')
@jwt_required()
def protected():
    x = getattr(current_identity, 'id')     # 'x' postaje ID usera čiji je token prosljeđen u auth header
    print("ja printam: {}".format(x))
    return '%s' % current_identity


api.add_resource(UserRegister, '/register')                     # stvara endpoint -> /register
api.add_resource(Notes, '/notes/<int:user_id>')                 # all notes from logged user
api.add_resource(Note, '/note/<int:id>')                        # specific note, supports get,post,put,del
api.add_resource(Weather, '/weather/<string:city_name>')        # trimmed info about weather from foreign API
api.add_resource(Crops, '/crops')                               # all crops
api.add_resource(Crop, '/crop/<string:crop_name>')              # crop basic info
api.add_resource(CropData, '/cropdata/<string:crop_name>')      # crop datasheet
api.add_resource(CropEco, '/cropeco/<string:crop_name>')        # crop ecology data
api.add_resource(CropCult, '/cropcult/<string:crop_name>')      # crop cultivation data
api.add_resource(ActionCal, '/actioncalendar')                  # all data from action calendar
api.add_resource(CropAction, '/actioncalendar/<string:crop_name>')              # specific data from action cal
api.add_resource(MedianValues, '/alg/<string:city_name>/<string:crop_name>')    # "how good is to plant specific
# plant in a specific city this week


if __name__ == '__main__':
    app.run()
