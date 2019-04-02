import mysql.connector
from flask_restful import Resource


mysql_config = {
    'user': 'root',
    'password': 'sifra321',
    'host': '127.0.0.1',
    'database': 'agro2',
    'raise_on_warnings': True
}


class ActionCal(Resource):

    def get(self):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT t1.*, t2.name FROM action_calendar as t1 LEFT JOIN crop as t2" \
                " ON t1.crop_id = t2.id"
        cursor.execute(query)

        data_from_cal = []
        for row in cursor:
            data_from_cal.append({
                'crop_name': row[4],
                'action': row[2],
                'month': row[3]
            })
        return {'data': data_from_cal}


class CropAction(Resource):
    def get(self, crop_name):
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT t1.*, t2.name FROM action_calendar as t1 INNER JOIN crop as t2" \
                " ON t1.crop_id = t2.id WHERE t2.name=%s"
        cursor.execute(query, (crop_name,))

        data_from_cal = []
        for row in cursor:
            data_from_cal.append({
                'crop_name': row[4],
                'action': row[2],
                'month': row[3]
            })
        return {'data': data_from_cal}
