import mysql.connector
from flask_restful import Resource


mysql_config = {
    'user': 'root',
    'password': 'sifra321',
    'host': '127.0.0.1',
    'database': 'agro2',
    'raise_on_warnings': True
}


class Crop(Resource):
    def get(self, crop_name):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM crop WHERE name=%s"
        cursor.execute(query, (crop_name,))

        for row in cursor:
            crop = {
                'name': row[1],
                'common_names': row[2],
                'description': row[3],
                'uses': row[4],
                'growing_period': row[5],
                'further_info': row[6]
            }
        connection.close()
        return crop


class CropData(Resource):
    def get(self, crop_name):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM crop_data WHERE crop_id=(SELECT id FROM crop WHERE name=%s)"
        cursor.execute(query, (crop_name,))

        for row in cursor:
            crop = {
                'life_form': row[1],
                'habit': row[2],
                'life_span': row[3],
                'physiology': row[4],
                'category': row[5],
                'plant_attributes': row[6],
                'crop_name': crop_name
            }
        connection.close()
        return crop


class CropEco(Resource):
    def get(self, crop_name):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM crop_eco WHERE crop_id=(SELECT id FROM crop WHERE name=%s)"
        cursor.execute(query, (crop_name,))

        for row in cursor:
            crop = {
                'req_temp_min_opt': row[2],
                'req_temp_max_opt': row[3],
                'req_temp_min_abs': row[4],
                'req_temp_max_abs': row[5],
                'annual_rainfal_min_opt': row[6],
                'annual_rainfal_max_opt': row[7],
                'annual_rainfal_min_abs': row[8],
                'annual_rainfal_max_abs': row[9],
                'soil_ph_opt_min': row[10],
                'soil_ph_opt_max': row[11],
                'soil_ph_abs_min': row[12],
                'soil_ph_abs_max': row[13],
                'light_intensity': row[14],
                'soil_depth_opt_min': row[15],
                'soil_depth_opt_max': row[16],
                'soil_depth_abs_min': row[17],
                'soil_depth_abs_max': row[18],
                'soil_texture_opt': row[19],
                'soil_texture_abs': row[20],
                'soil_fert_opt': row[21],
                'soil_fert_abs': row[22],
                'soil_salinity_opt': row[23],
                'soil_salinity_abs': row[24],
                'soil_drainage_opt': row[25],
                'soil_drainage_abs': row[26],
                'crop_name': crop_name
            }
        connection.close()
        return crop


class CropCult(Resource):
    def get(self, crop_name):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM crop_cult WHERE crop_id=(SELECT id FROM crop WHERE name=%s)"
        cursor.execute(query, (crop_name,))

        for row in cursor:
            crop = {
                'product_system': row[2],
                'crop_cycle_min': row[3],
                'crop_cycle_max': row[4],
                'crop_name': crop_name
            }
        connection.close()
        return crop


class Crops(Resource):
    def get(self):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT * FROM crop"
        cursor.execute(query)

        crops = []
        for row in cursor:
            crops.append({
                'name': row[1],
                'common_names': row[2],
                'description': row[3],
                'uses': row[4],
                'growing_period': row[5],
                'further_info': row[6]
            })

        connection.close()
        return {'crops': crops}

