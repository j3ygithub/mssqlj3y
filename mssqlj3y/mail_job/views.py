from django.shortcuts import render
import pyodbc
import pandas
from .forms import MailJobForm
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
            event = form.cleaned_data['event']
        try:
            # do script here
            context['message'] = 'Finished.'
        except:
            context['message'] = 'Failed.'
    # a query-all script
    query_string = """
    exec mail_job.dbo.show_mail_job '',''
    ;
    """
    response = exec_sp(
        driver='{SQL Server}',
        server='tcp:150.117.123.35',
        database='mail_job',
        uid='jimmy_lin',
        pwd='Chief+26576688@',
        query_header='set nocount on;',
        query_string=query_string,
    )
    df = pandas.DataFrame(tuple(row) for row in response)
    df.columns = ['查詢結果', '項次', '部門', '類型', '事件', '日期', '週期', '假日例外', '標題', '內容', '收件人', '起始日期', '終止日期', '建立人', '修改者', '修改日期', ]
    df.index = pandas.RangeIndex(start=1, stop=len(df)+1, step=1)
    df = df[['部門', '類型', '事件', '日期', '週期', '假日例外', '標題', '內容', '收件人']]
    df_html = df.to_html(justify='left')
    context['result']['目前設置'] = df_html
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