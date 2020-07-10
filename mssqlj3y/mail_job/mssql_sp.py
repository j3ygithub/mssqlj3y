import pyodbc
from secret.mail_job.mssql_sp import login_info


def exec_query(query_string, query_header='set nocount on;'):

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
    response_query_all = exec_query(query_string=query_string)
    return response_query_all


def sp_show_mail_job_1(seq='', created_by=''):

    query_string = f"exec mail_job.dbo.show_mail_job_1 @seq='{seq}', @create_by='{created_by}' ;"
    response_query_all = exec_query(query_string=query_string)
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
    response_insert = exec_query(query_string=query_string)
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
    response_update = exec_query(query_string=query_string)
    return response_update


def sp_do_mail_job_onetime(seq=''):

    query_string = (
        "exec mail_job.dbo.do_mail_job_onetime "
        f"@seq_action='{seq}' "
        ";"
    )
    response_do_test = exec_query(query_string=query_string)
    return response_do_test


# 2020-07-10 new store procedure
def sp_insert_mail_job_1(
    department, event_class, event, note_date, period,
    weekend_flag, subject, body, recipient, created_by,
    stop_date, recipient_add
):
    """
    The equivalent SQL example:

    exec mail_job.dbo.insert_mail_job_1
    @department='T31',
    @event_class='jack_test',
    @event='測試最終日發信三次',
    @note_date='2020-07-08',
    @period='每日',
    @weekend_flag='F',
    @subject='測試最終日發信三次',
    @body='jack_test',
    @recipient='jack_chang@chief.com.tw',
    @create_by='jack_chang',
    @stop_date='2020-07-13 23:59:59',  --stop_date必須大於notify_date及getdate()，所以設定需為YYYY-MM-DD 23:59:59
    @recipient_add='發信時間為&&，距發信截止日還有$$天'  --&&及$$為變數分別代表convert(varchar(16),getdate(),120)及notify_date-->stop_date的天數
    """
    query_string = (
        "exec mail_job.dbo.insert_mail_job_1 "
        f"@department='{department}', "
        f"@event_class='{event_class}', "
        f"@event='{event}', "
        f"@note_date='{note_date}', "
        f"@period='{period}', "
        f"@weekend_flag='{weekend_flag}', "
        f"@subject='{subject}', "
        f"@body='{body}', "
        f"@recipient='{recipient}', "
        f"@create_by='{created_by}', "
        f"@stop_date='{stop_date}', "
        f"@recipient_add='{recipient_add} '"
        ";"
    )
    response_insert = exec_query(query_string=query_string)
    return response_insert


def sp_update_mail_job_1(
    seq='', department='', event_class='', event='', note_date='', period='',
    weekend_flag='', subject='', body='', recipient='', stop_date='', updated_by='',
    mail_count='', mode_send='', recipient_add='',
):
    """
    The equivalent SQL example:

    exec mail_job.dbo.update_mail_job_1
    @seq='182',
    @department='',
    @event_class='',
    @event='',
    @note_date='',
    @period='',
    @weekend_flag='',
    @subject='',
    @body='Dear all, 本email為測試發信最終日要於8,12,14時發送通知',
    @recipient='jack_chang@chief.com.tw',
    @stop_date='2020-07-09 23:59:59',  --stop_date必須大於notify_date及getdate()，所以設定需為YYYY-MM-DD 23:59:59
    @update_by='jack_chang',
    @mail_count='',
    @mode_send='',  --0為正常發信模式，1為convert(varchar(10),stop_date,120)=convert(varchar(10),getdate(),120)時會於8、12、14時發信
    @recipient_add='發信時間為&&，距發信截止日還有$$天'  --&&及$$為變數分別代表convert(varchar(16),getdate(),120)及notify_date-->stop_date的天數
    """
    query_string = (
        "exec mail_job.dbo.update_mail_job_1 "
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
        f"@update_by='{updated_by}', "
        f"@mail_count='{mail_count}', "
        f"@mode_send='{mode_send}', "
        f"@recipient_add='{recipient_add}' "
        ";"
    )
    response_update = exec_query(query_string=query_string)
    return response_update


def sp_show_mail_job_2(seq='', created_by=''):

    query_string = f"exec mail_job.dbo.show_mail_job_2 @seq='{seq}', @create_by='{created_by}' ;"
    response_query_all = exec_query(query_string=query_string)
    return response_query_all


def sp_do_mail_job_onetime_1(seq=''):

    query_string = (
        "exec mail_job.dbo.do_mail_job_onetime_1 "
        f"@seq_action='{seq}' "
        ";"
    )
    response_do_test = exec_query(query_string=query_string)
    return response_do_test
