# import mysql.connector
# from mysql.connector import errorcode
#
#
# mysql_config = {
#     'user': 'root',
#     'password': 'sifra321',
#     'host': '127.0.0.1',
#     'database': 'agro',
#     'raise_on_warnings': True
# }
#
# try:
#     cnx = mysql.connector.connect(**mysql_config)
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Wrong username or password (for db).")
#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does NOT exist.")
#     else:
#         print(err)
#
#
# def find_by_username(username):
#
#     cnx = mysql.connector.connect(**mysql_config)
#     cursor = cnx.cursor()
#     query = ("SELECT * FROM korisnik WHERE korisnicko_ime=?")
#     result = cursor.execute(query, (username,))
#     row = result.fetchone()
#     if row:
#         user = (*row)
#     else:
#         user = None
#
#     # return user
#
#     for (id, korisnicko_ime, email, lozinka, avatar, uloga) in cursor:
#         if korisnicko_ime == username:
#             user1 = {
#                 "id": id,
#                 "korisnicko_ime": korisnicko_ime,
#                 "email": email,
#                 "lozinka": lozinka,
#                 "avatar": avatar,
#                 "uloga": uloga
#             }
#         cursor.close()
#     cnx.close()
#
#     return user1
#
#
# def find_by_id(user_id):
#     try:
#         cnx = mysql.connector.connect(**mysql_config)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Wrong username or password (for db).")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does NOT exist.")
#         else:
#             print(err)
#
#     cursor = cnx.cursor()
#     query = ("SELECT * FROM korisnik")
#     cursor.execute(query)
#
#     for (id, korisnicko_ime, email, lozinka, avatar, uloga) in cursor:
#         if id == user_id:
#             user1 = {
#                 "id": id,
#                 "korisnicko_ime": korisnicko_ime,
#                 "email": email,
#                 "lozinka": lozinka,
#                 "avatar": avatar,
#                 "uloga": uloga
#             }
#         cursor.close()
#     cnx.close()
#     return user1
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
