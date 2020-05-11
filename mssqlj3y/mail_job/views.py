from django.shortcuts import render
import pyodbc
import pandas
from .forms import SetupForm, LookupForm, MailJobForm
from secret.database import login_info
from django.utils import timezone
# Create your views here.


def setup(request):
    context = {
        'name': 'setup',
        'verbose_name': 'Setup',
        'form': None,
        'message': '',
    }
    if request.method != 'POST':
        form = SetupForm()
        context['form'] = form
    else:
        form = SetupForm(request.POST)
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
            if request.user.is_authenticated:
                created_by = request.user
            else:
                created_by = request.META.get('REMOTE_ADDR')
            followed_action = form.cleaned_data['followed_action']
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
            @create_by='{created_by}'
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
    return render(request, 'mail_job/setup.html', context)


def lookup(request):
    context = {
        'view_name': 'lookup',
        'verbose_name': 'Lookup',
        'message': '',
        'result_html': {},
        'form': LookupForm(),
    }
    if request.method == 'POST':
        form = LookupForm(request.POST)
        context['form'] = form
        if form.is_valid():
            department = form.cleaned_data['department']
        try:
            if department == 'all':
                department = ''            
            # call query sp
            query_string = f"""
            exec mail_job.dbo.show_mail_job
            @seq='',
            @department='{department}'
            ;
            """
            response_query_all = exec_sp(
                driver=login_info['driver'],
                server=login_info['server'],
                database=login_info['database'],
                uid=login_info['uid'],
                pwd=login_info['pwd'],
                query_header='set nocount on;',
                query_string=query_string,
            )
            if response_query_all[0][0] == '查詢成功':
                df = pandas.DataFrame(tuple(row) for row in response_query_all)
                df.columns = ['查詢結果', '項次', '部門', '事件類型', '事件描述', '通知起始日', '週期', '假日除外', '郵件主旨', '郵件內容', '收件人', '建立時間', '規則終止日', '建立者', '修改者', '修改日期', ]
                for index, row in df.iterrows():
                    # added a href
                    df.loc[index, '動作'] = f'<a href="/mail_job/{row["項次"]}/change/">修改</a>/<a href="/mail_job/{row["項次"]}/delete/">註銷</a>'
                    # merge the period and the weekend flag
                    if row['週期'] == '每日' and row['假日除外'] == 'T':
                        df.loc[index, '週期'] = '每日(假日除外)'
                df = df[['動作', '部門', '事件類型', '事件描述', '通知起始日', '週期', '郵件主旨', '郵件內容', '收件人', '建立者', '建立時間']]

                df = df.sort_values(by=['建立時間'], ascending=False)
                df.index = pandas.RangeIndex(start=1, stop=len(df)+1, step=1)
                df_html = df.to_html(justify='left', classes='j3y-df table table-responsive', escape=False)
                context['result_html']['目前設置'] = df_html
            else:
                pass
            context['message'] = response_query_all[0][0]
        except:
            context['message'] = 'Failed.'
    return render(request, 'mail_job/lookup.html', context)


def change(request, seq):
    context = {
        'view_name': 'change',
        'verbose_name': 'Change',
        'message': '',
        'form': None,
        'delete_url': f'/mail_job/{seq}/delete/',
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
            if request.user.is_authenticated:
                updated_by = request.user
            else:
                updated_by = request.META.get('REMOTE_ADDR')
            if period == '每日(假日除外)':
                period = '每日'
                weekend_flag = 'T'
            else:
                weekend_flag = 'F'
        try:
            # call update sp
            query_string = f"""
            exec mail_job.dbo.update_mail_job
            @seq='{seq}',
            @department='{department}',
            @event_class='{event_class}',
            @event='{event}',
            @note_date='{note_date}',
            @period='{period}',
            @weekend_flag='{weekend_flag}',
            @subject='{subject}',
            @body='{body}',
            @recipient='{recipient}',
            @stop_date='',
            @update_by='{updated_by}'
            ;
            """
            response_query_all = exec_sp(
                driver=login_info['driver'],
                server=login_info['server'],
                database=login_info['database'],
                uid=login_info['uid'],
                pwd=login_info['pwd'],
                query_header='set nocount on;',
                query_string=query_string,
            )
            context['message'] = response_query_all[0][0]
        except:
            context['message'] = 'Failed.'
    else:
        try:
            # call query sp
            query_string = f"""
            exec mail_job.dbo.show_mail_job
            @seq='{seq}',
            @department=''
            ;
            """
            response_query_all = exec_sp(
                driver=login_info['driver'],
                server=login_info['server'],
                database=login_info['database'],
                uid=login_info['uid'],
                pwd=login_info['pwd'],
                query_header='set nocount on;',
                query_string=query_string,
            )
        except:
            context['message'] = '未知的錯誤，無法返回該筆資料。'
        try:
            df = pandas.DataFrame(tuple(row) for row in response_query_all)
            if len(response_query_all) == 1 and response_query_all[0][0] == '查詢成功':
                df.columns = ['查詢結果', '項次', '部門', '事件類型', '事件描述', '通知起始日', '週期', '假日除外', '郵件主旨', '郵件內容', '收件人', '建立時間', '規則終止日', '建立者', '修改者', '修改日期', ]
                for index, row in df.iterrows():
                    if row['週期'] == '每日' and row['假日除外'] == 'T':
                        df.loc[index, '週期'] = '每日(假日除外)'
                df = df.sort_values(by=['建立時間'], ascending=False)
                form = MailJobForm(
                    initial={
                        'department': df.loc[0, '部門'],
                        'event_class': df.loc[0, '事件類型'],
                        'event': df.loc[0, '事件描述'],
                        'note_date': df.loc[0, '通知起始日'],
                        'period': df.loc[0, '週期'],
                        'subject': df.loc[0, '郵件主旨'],
                        'body': df.loc[0, '郵件內容'],
                        'recipient': df.loc[0, '收件人'],
                    },
                )
                context['form'] = form
                context['message'] = '以下為目前的設置，請填入欲修改的部分後送出。'
            else:
                context['message'] = '查無這筆資料，請確認該資料是否已被刪除。'
        except:
            context['message'] = '未知的錯誤，無法返回資料。'
    return render(request, 'mail_job/change.html', context)


def delete(request, seq):
    context = {
        'view_name': 'delete',
        'verbose_name': 'Delete',
        'message': '',
    }
    if request.method == 'POST':
        try:
            # call update sp
            query_string = f"""
            exec mail_job.dbo.update_mail_job
            @seq='{seq}',
            @department='',
            @event_class='',
            @event='',
            @note_date='',
            @period='',
            @weekend_flag='',
            @subject='',
            @body='',
            @recipient='',
            @stop_date='{timezone.localtime(timezone.now()).date()}',
            @update_by=''
            ;
            """
            response_query_all = exec_sp(
                driver=login_info['driver'],
                server=login_info['server'],
                database=login_info['database'],
                uid=login_info['uid'],
                pwd=login_info['pwd'],
                query_header='set nocount on;',
                query_string=query_string,
            )
            context['message'] = response_query_all[0][0]
        except:
            context['message'] = 'Failed.'
    else:
        pass
    return render(request, 'mail_job/delete.html', context)


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