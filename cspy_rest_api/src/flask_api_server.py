import os
import sqlite3

from flask import Flask, request, g
from flask_restful import Resource, Api

cs_py_server = Flask(__name__)
cs_py_rest_api = Api(cs_py_server)
cs_py_server.config['DATABASE'] = os.path.join(cs_py_server.root_path, '..', 'users_and_matches.db')

# ---------------------------


# database connection handling
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(cs_py_server.config['DATABASE'])
    return g.sqlite_db


# makes sure required tables exist; if not, create them
def server_sql_setup(sql_db):
    create_users_table_sql = '''CREATE TABLE IF NOT EXISTS all_users (User_SteamID INTEGER, "Match Count" INTEGER)'''

    create_matches_table_sql = '''CREATE TABLE IF NOT EXISTS all_matches (Match_ID INTEGER PRIMARY KEY, 
                                                                          User_SteamID INTEGER, Start INTEGER, End Integer, 
                                                                          'Round Count' INTEGER, Map TEXT, Rating1 REAL,
                                                                          HSR REAL, MDC REAL, KPR REAL, KAS REAL, 
                                                                          KDR REAL, KDA REAL, MEAN REAL, 
                                                                          CT_Rating1 REAL, CT_HSR REAL, CT_MDC REAL, 
                                                                          CT_KPR REAL, CT_KAS REAL, CT_KDR REAL, 
                                                                          CT_KDA REAL, CT_MEAN REAL, T_Rating1 REAL, 
                                                                          T_HSR REAL, T_MDC REAL, T_KPR REAL, T_KAS REAL, 
                                                                          T_KDR REAL, T_KDA REAL, T_MEAN REAL,
                                                                          FOREIGN KEY (User_SteamID) 
                                                                          REFERENCES all_users(User_SteamID))'''

    db_cursor = sql_db.cursor()
    db_cursor.execute(create_users_table_sql)
    db_cursor.execute(create_matches_table_sql)
    sql_db.commit()
    print("SQL Table Check Passed")

# ---------------------------


class MatchDataApi(Resource):
    def post(self):
        print(request.headers)
        print(request.is_json)
        print(request.get_json())
        return 'Data Accepted', 202


cs_py_rest_api.add_resource(MatchDataApi, '/api')


# TODO: Only for testing, remove for deployment. For deployment, use PythonAnywhere.
if __name__ == '__main__':
    startup_conn = sqlite3.connect(cs_py_server.config['DATABASE'])
    server_sql_setup(startup_conn)
    cs_py_server.run(debug=False)