import requests, json
from flask_restful import Resource


class Weather(Resource):

    @classmethod
    def get_weather_api(cls, city_name):
        api_url_base = 'http://meteo.pointjupiter.co/'
        headers = {'Content-Type': 'application/json'}
        api_url = '{0}{1}'.format(api_url_base, city_name)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        return {'message': 'Something went wrong with fetching API'}, 500

    def get(self, city_name):
        dataa = self.get_weather_api(city_name)

        for obj in dataa['data']:
            for value in obj['forecast']:
                value.pop('dewpoint', None)
                value.pop('fog', None)
                value.pop('h0m', None)
                value.pop('mlcape', None)
                value.pop('mslp', None)
                value.pop('t850', None)
                value.pop('snowpct', None)
                value.pop('tstorm', None)
                value.pop('tstormpct', None)
                value.pop('wdir', None)

        return dataa

    # daljnji algoritmi za sjetveni kalendar ovdje ili posebni file?

