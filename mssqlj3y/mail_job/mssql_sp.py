import pyodbc
from secret.mail_job.mssql_sp import login_info


def exec_sp(query_string, query_header='set nocount on;'):
    driver = login_info['driver']
    server = login_info['server']
    database = login_info['database']
    uid = login_info['uid']
    pwd = login_info['pwd']
    connect_string = f"""DRIVER={driver}; SERVER={server}; DATABASE={database}; UID={uid}; PWD={pwd};"""
    cnxn = pyodbc.connect(connect_string, autocommit=True)
    cursor = cnxn.cursor()
    cursor.execute(query_header + query_string)
    response = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return response