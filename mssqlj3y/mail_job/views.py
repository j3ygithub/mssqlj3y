from django.shortcuts import render
import pyodbc
import pandas
from .forms import MailJobForm
from .database import login_info
# Create your views here.


def index(request):
    context = {
        'query_param_cookie': {},
        'message': '',
        'result': {},
        'form': MailJobForm(),
    }
    if request.method == 'POST':
        form = MailJobForm(request.POST)
        context['form'] = form
        if form.is_valid():
            department = form.cleaned_data['department']
            event_class = form.cleaned_data['event_class']
            event = form.cleaned_data['event']
            note_date = form.cleaned_data['note_date']
            period = form.cleaned_data['period']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient = form.cleaned_data['recipient']
            followed_action = form.cleaned_data['followed_action']
            create_by = request.META.get('REMOTE_ADDR')
            if period == '每日(假日除外)':
                period = '每日'
                weekend_flag = 'T'
            else:
                weekend_flag = 'F'
        try:
            # call insert sp
            query_string = f"""
            exec mail_job.dbo.insert_mail_job 
            @department='{department}',
            @event_class='{event_class}',
            @event='{event}',
            @note_date='{note_date}',
            @period='{period}',
            @weekend_flag='{weekend_flag}',
            @subject='{subject}',
            @body='{body}',
            @recipient='{recipient}',
            @create_by='{create_by}'
            ;
            """
            response_insert = exec_sp(
                driver=login_info['driver'],
                server=login_info['server'],
                database=login_info['database'],
                uid=login_info['uid'],
                pwd=login_info['pwd'],
                query_header='set nocount on;',
                query_string=query_string,
            )
            # end
            context['message'] = response_insert[0][0]
        except:
            context['message'] = 'Failed.'
        try:
            # call do-test sp
            if followed_action == '立即發出一封測試信件' and response_insert[0][0] == '新增成功':
                seq = response_insert[0][1]
                query_string = f"""
                exec mail_job.dbo.do_mail_job_onetime
                @seq_action='{seq}'
                ;
                """
                response_do_test = exec_sp(
                    driver=login_info['driver'],
                    server=login_info['server'],
                    database=login_info['database'],
                    uid=login_info['uid'],
                    pwd=login_info['pwd'],
                    query_header='set nocount on;',
                    query_string=query_string,
                )
            # end
            if response_do_test:
                context['message'] += f'\n{response_do_test}'
        except:
            pass
    # # call query sp
    # query_string = """
    # exec mail_job.dbo.show_mail_job '',''
    # ;
    # """
    # response_query_all = exec_sp(
    #     driver=login_info['driver'],
    #     server=login_info['server'],
    #     database=login_info['database'],
    #     uid=login_info['uid'],
    #     pwd=login_info['pwd'],
    #     query_header='set nocount on;',
    #     query_string=query_string,
    # )
    # # end
    # df = pandas.DataFrame(tuple(row) for row in response_query_all)
    # df.columns = ['查詢結果', '項次', '部門', '事件類型', '事件描述', '通知起始日', '週期', '假日', '郵件主旨', '郵件內容', '收件人', '建立時間', '規則終止日', '建立者', '修改者', '修改日期', ]
    # df = df[['部門', '事件類型', '事件描述', '通知起始日', '週期', '假日', '郵件主旨', '郵件內容', '收件人', '建立者', '建立時間']]
    # df = df.sort_values(by=['建立時間'], ascending=False)
    # df.index = pandas.RangeIndex(start=1, stop=len(df)+1, step=1)
    # df_html = df.to_html(justify='left')
    # context['result']['目前設置'] = df_html
    return render(request, 'mail_job/index.html', context)


def exec_sp(driver, server, database, uid, pwd, query_header, query_string):
    driver= driver
    server = server
    database = database
    uid = uid
    pwd = pwd
    connect_string = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    UID={uid};
    PWD={pwd};
    """
    cnxn = pyodbc.connect(connect_string, autocommit=True)
    cursor = cnxn.cursor()
    query_header = query_header
    query_string = query_string
    query = query_header + query_string
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return response