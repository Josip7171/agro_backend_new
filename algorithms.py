from flask_restful import Resource
import datetime

from weather import Weather
from crop import CropEco
from action_calendar import CropAction


class MedianValues(Resource):

    def get(self, city_name, crop_name):

        crop = CropEco()
        crop_data = crop.get(crop_name)

        weather = Weather()
        weather_data = weather.get(city_name)

        cropaction = CropAction()
        cropaction_data = cropaction.get(crop_name)

        final_result = []
        hour_collection = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                           '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

        curr_month = datetime.datetime.now().strftime("%B").lower()

        for obj in weather_data['data']:
            temp_data = []
            humid_data = []
            calendar_agrees_planting = False
            calendar_agrees_transplanting = False
            calendar_agrees_harvesting = False
            wspd_test_passed = True
            gust_test_passed = True
            prec_test_passed = True
            count = 0

            # check if calendar agrees that it is time for PLANTING/TRANSPLANTING/HARVESTING
            planting_month_collection = []
            transplant_month_collection = []
            harvest_month_collection = []
            for objj in cropaction_data['data']:
                if objj['action'] == 'planting':
                    planting_month_collection.append(objj['month'])
                if objj['action'] == 'transplant':
                    transplant_month_collection.append(objj['month'])
                if objj['action'] == 'harvest':
                    harvest_month_collection.append(objj['month'])

            for val in planting_month_collection:
                if val == curr_month:
                    calendar_agrees_planting = True
            for val in transplant_month_collection:
                if val == curr_month:
                    calendar_agrees_transplanting = True
            for val in harvest_month_collection:
                if val == curr_month:
                    calendar_agrees_harvesting = True

            # check if temp/humid is good for crop and if there is no wind/rain/gust
            for value in obj['forecast']:
                if value['hour'] == '07:00' or value['hour'] == '14:00':
                    temp_data.append(int(value['temperature']))
                    humid_data.append(int(value['humidity']))
                elif value['hour'] == '21:00':
                    temp_data.append(int(value['temperature']))
                    temp_data.append(int(value['temperature']))
                    humid_data.append(int(value['humidity']))
                    humid_data.append(int(value['humidity']))

                for x in hour_collection:
                    if int(value['wspd']) >= 10:
                        wspd_test_passed = False
                    if int(value['gust']) >= 12:
                        gust_test_passed = False
                    if float(value['prec']) > 1:
                        count+=1
                    if count >= 3:
                        prec_test_passed = False

            # this part talks about what temperature says about planting
            temp_depending_measure = 0
            avg_temp = sum(temp_data)/len(temp_data)
            opt_temp = (crop_data['req_temp_min_opt'] - crop_data['req_temp_max_opt']) / 2
            if avg_temp < opt_temp:
                x1 = opt_temp - crop_data['req_temp_min_abs']
                x2 = avg_temp - crop_data['req_temp_min_abs']
                temp_depending_measure = x2 / x1 * 100
            elif avg_temp > opt_temp:
                x1 = crop_data['req_temp_max_abs'] - opt_temp
                x2 = crop_data['req_temp_max_abs'] - avg_temp
                temp_depending_measure = x2 / x1 * 100
            elif avg_temp == opt_temp:
                temp_depending_measure = 100

            # this part talks about what humidity says about planting
            avg_humid = sum(humid_data)/len(humid_data)
            humid_depending_measure = 0
            if 70 >= avg_humid >= 30:
                humid_depending_measure = 100
            elif (30 > avg_humid > 15) or (85 > avg_humid > 70):
                humid_depending_measure = 50

            # check if any of temp/humid "planting" tests failed
            if humid_depending_measure != 0 and temp_depending_measure != 0:
                final_humid_temp_measure = (humid_depending_measure + temp_depending_measure) / 2
            else:
                final_humid_temp_measure = 0

            final_result.append({
                'date': obj['date'],
                'weekday': obj['weekday'],
                'calendar_agrees_on_planting': calendar_agrees_planting,
                'calendar_agrees_on_transplant': calendar_agrees_transplanting,
                'calendar_agrees_on_harvest': calendar_agrees_harvesting,
                'temp_depending_measure': temp_depending_measure,
                'humid_depending_measure': humid_depending_measure,
                'final_humid_temp_measure': final_humid_temp_measure,
                'wspd_test_passed': wspd_test_passed,
                'gust_test_passed': gust_test_passed,
                'prec_test_passed': prec_test_passed
            })

        return {'data': final_result}
