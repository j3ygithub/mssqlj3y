import pyodbc
from secret.mail_job.mssql_sp import login_info


def exec_sp(query_string, query_header='set nocount on;'):

    driver = login_info['driver']
    server = login_info['server']
    database = login_info['database']
    uid = login_info['uid']
    pwd = login_info['pwd']
    connect_string = f'DRIVER={driver}; SERVER={server}; DATABASE={database}; UID={uid}; PWD={pwd};'
    cnxn = pyodbc.connect(connect_string, autocommit=True)
    cursor = cnxn.cursor()
    cursor.execute(query_header + query_string)
    response = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return response

def sp_show_mail_job(seq='', department=''):

    query_string = f"exec mail_job.dbo.show_mail_job @seq='{seq}', @department='{department}' ;"
    response_query_all = exec_sp(query_string=query_string)
    return response_query_all

def sp_show_mail_job_1(seq='', created_by=''):

    query_string = f"exec mail_job.dbo.show_mail_job_1 @seq='{seq}', @create_by='{created_by}' ;"
    response_query_all = exec_sp(query_string=query_string)
    return response_query_all

def sp_insert_mail_job(
    department, event_class, event, note_date, period,
    weekend_flag, subject, body, recipient, created_by
):

    query_string = (
        "exec mail_job.dbo.insert_mail_job "
        f"@department='{department}', "
        f"@event_class='{event_class}', "
        f"@event='{event}', "
        f"@note_date='{note_date}', "
        f"@period='{period}', "
        f"@weekend_flag='{weekend_flag}', "
        f"@subject='{subject}', "
        f"@body='{body}', "
        f"@recipient='{recipient}', "
        f"@create_by='{created_by}' "
        ";"
    )
    response_insert = exec_sp(query_string=query_string)
    return response_insert

def sp_update_mail_job(
    seq='', department='', event_class='', event='', note_date='', period='',
    weekend_flag='', subject='', body='', recipient='', stop_date='', updated_by=''
):
    
    query_string = (
        "exec mail_job.dbo.update_mail_job "
        f"@seq='{seq}', "
        f"@department='{department}', "
        f"@event_class='{event_class}', "
        f"@event='{event}', "
        f"@note_date='{note_date}', "
        f"@period='{period}', "
        f"@weekend_flag='{weekend_flag}', "
        f"@subject='{subject}', "
        f"@body='{body}', "
        f"@recipient='{recipient}', "
        f"@stop_date='{stop_date}', "
        f"@update_by='{updated_by}' "
        ";"
    )   
    response_update = exec_sp(query_string=query_string)
    return response_update

def sp_do_mail_job_onetime(seq=''):

    query_string = (
        "exec mail_job.dbo.do_mail_job_onetime "
        f"@seq_action='{seq}' "
        ";"
    )
    response_do_test = exec_sp(query_string=query_string)
    return response_do_test