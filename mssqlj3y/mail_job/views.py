from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
import pandas
from .forms import SetupForm, MailJobForm
from .mssql_sp import exec_sp

# Create your views here.


def change_list(request, messages={}):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'messages': messages,
        'htmls': {},
    }
    try:
        # call query sp
        query_string = f"""exec mail_job.dbo.show_mail_job @seq='', @department='';"""
        response_query_all = exec_sp(query_string=query_string)
        if response_query_all[0][0] == '查詢成功':
            df = pandas.DataFrame(tuple(row) for row in response_query_all)
            df.columns = [
                '查詢結果',
                '項次',
                '部門',
                '事件類型',
                '事件描述',
                '通知起始日',
                '週期',
                '假日除外',
                '郵件主旨',
                '郵件內容',
                '收件人',
                '建立時間',
                '規則終止日',
                '建立者',
                '修改者',
                '修改日期',
            ]
            for index, row in df.iterrows():
                # added a href
                options = [
                    '<option value="">請選擇</option>',
                    f'<option value="/mail_job/{row["項次"]}/change/">修改</option>',
                    f'<option value="/mail_job/{row["項次"]}/delete/">註銷</option>',
                    f'<option value="/mail_job/{row["項次"]}/mail-test/">發測試信</option>',
                ]
                html_select = f'<select class="form-control" onchange="location = this.value;">{"".join(options)}</select>'
                html_form = f'<form autocomplete="off"><div class="form-group">{html_select}</div></form>'
                df.loc[index, '動作'] = html_form
                # merge the period and the weekend flag
                if row['週期'] == '每日' and row['假日除外'] == 'T':
                    df.loc[index, '週期'] = '每日(假日除外)'
            df = df[[
                '動作',
                '部門',
                '事件類型',
                '事件描述',
                '通知起始日',
                '週期',
                '郵件主旨',
                '郵件內容',
                '收件人',
                '建立者',
                '建立時間',
            ]]
            df = df.sort_values(by=['建立時間'], ascending=False)
            df.index = pandas.RangeIndex(start=1, stop=len(df) + 1, step=1)
            df_html = df.to_html(
                justify='left',
                classes=
                'j3y-df table table-light table-bordered table-striped table-responsive',
                escape=False,
            )
            context['htmls']['currently'] = df_html
        else:
            context['messages']['change_list'] = '未知的錯誤，返回的資料格式不正確。'
    except:
        context['messages']['change_list'] = '未知的錯誤，無法返回資料。'
        context['messages']['dashboard'] = '已成功發出測試信。'
    return render(request, 'mail_job/change_list.html', context)


def add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'form': None,
        'messages': {},
    }
    if request.method != 'POST':
        form = MailJobForm()
        context['form'] = form
        return render(request, 'mail_job/add.html', context)
    elif request.method == 'POST':
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
                created_by = request.user
            else:
                created_by = request.META.get('REMOTE_ADDR')
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
            response_insert = exec_sp(query_string=query_string)
            # end
            response_insert[0][0]
            if response_insert[0][0] == '新增成功':
                context['messages']['add'] = '已新增成功。'
                return change_list(request, messages=context['messages'])
            if response_insert[0][0] == '新增失敗，資料重覆，請確認':
                context['messages']['add'] = '與既有的資料重覆，新增失敗。'
        except:
            context['messages']['add'] = '未知的錯誤，返回的資料格式不正確。'
        return render(request, 'mail_job/add.html', context)


def change(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'messages': {},
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
            response_query_all = exec_sp(query_string=query_string)
            if response_query_all[0][0] == '修改成功':
                context['messages']['change'] = '已修改成功。'
        except:
            context['messages']['change'] = '未知的錯誤，返回的資料格式不正確。'
        return change_list(request, messages=context['messages'])
    else:
        try:
            # call query sp
            query_string = f"""
            exec mail_job.dbo.show_mail_job
            @seq='{seq}',
            @department=''
            ;
            """
            response_query_all = exec_sp(query_string=query_string)
        except:
            context['messages']['change'] = '未知的錯誤，無法返回該筆資料。'
        try:
            df = pandas.DataFrame(tuple(row) for row in response_query_all)
            if len(response_query_all
                   ) == 1 and response_query_all[0][0] == '查詢成功':
                df.columns = [
                    '查詢結果',
                    '項次',
                    '部門',
                    '事件類型',
                    '事件描述',
                    '通知起始日',
                    '週期',
                    '假日除外',
                    '郵件主旨',
                    '郵件內容',
                    '收件人',
                    '建立時間',
                    '規則終止日',
                    '建立者',
                    '修改者',
                    '修改日期',
                ]
                for index, row in df.iterrows():
                    try:
                        if not str(request.user) == row['建立者'] and not request.user.is_staff:
                            context['messages']['change'] = '你只能修改自己建立的 Mail Job。'
                            return change_list(request, messages=context['messages'])
                    except:
                        pass
                    if row['週期'] == '每日' and row['假日除外'] == 'T':
                        df.loc[index, '週期'] = '每日(假日除外)'
                df = df.sort_values(by=['建立時間'], ascending=False)
                form = MailJobForm(initial={
                    'department': df.loc[0, '部門'],
                    'event_class': df.loc[0, '事件類型'],
                    'event': df.loc[0, '事件描述'],
                    'note_date': df.loc[0, '通知起始日'],
                    'period': df.loc[0, '週期'],
                    'subject': df.loc[0, '郵件主旨'],
                    'body': df.loc[0, '郵件內容'],
                    'recipient': df.loc[0, '收件人'],
                }, )
                context['form'] = form
                context['messages']['change'] = '以下為目前的設置，請填入欲修改的部分後送出。'
            else:
                context['messages']['change'] = '查無這筆資料，請確認該資料是否已被刪除。'
        except:
            context['messages']['change'] = '未知的錯誤，無法返回資料。'
        return render(request, 'mail_job/change.html', context)


def delete(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'messages': {},
    }
    try:
        # call query sp
        query_string = f"""
        exec mail_job.dbo.show_mail_job
        @seq='{seq}',
        @department=''
        ;
        """
        response_query_all = exec_sp(query_string=query_string)
    except:
        context['messages']['change_list'] = '未知的錯誤，無法返回該筆資料。'
    try:
        df = pandas.DataFrame(tuple(row) for row in response_query_all)
        if len(response_query_all) == 1 and response_query_all[0][0] == '查詢成功':
            df.columns = [
                '查詢結果',
                '項次',
                '部門',
                '事件類型',
                '事件描述',
                '通知起始日',
                '週期',
                '假日除外',
                '郵件主旨',
                '郵件內容',
                '收件人',
                '建立時間',
                '規則終止日',
                '建立者',
                '修改者',
                '修改日期',
            ]
            for index, row in df.iterrows():
                try:
                    if not str(request.user
                               ) == row['建立者'] and not request.user.is_staff:
                        context['messages']['delete'] = '你只能註銷自己建立的 Mail Job。'
                        return change_list(request, messages=context['messages'])
                except:
                    pass
    except:
        context['messages']['delete'] = '未知的錯誤，無法返回該筆資料。'
    if request.method == 'POST':
        if request.user.is_authenticated:
            updated_by = request.user
        else:
            updated_by = request.META.get('REMOTE_ADDR')
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
            @update_by='{updated_by}'
            ;
            """
            response_query_all = exec_sp(query_string=query_string)
            if response_query_all[0][0] == '修改成功':
                context['messages']['delete'] = '已註銷成功。'
            else:
                context['messages']['delete'] = '註銷失敗，該資料可能已不存在。'
        except:
            context['messages']['delete'] = '未知的錯誤，無法返回資料。'
        return change_list(request, messages=context['messages'])
    else:
        return render(request, 'mail_job/delete.html', context)


def mail_test(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'messages': {},
    }
    try:
        # call query sp
        query_string = f"""
        exec mail_job.dbo.show_mail_job
        @seq='{seq}',
        @department=''
        ;
        """
        response_query_all = exec_sp(query_string=query_string)
    except:
        context['messages']['change_list'] = '未知的錯誤，無法返回該筆資料。'
    try:
        df = pandas.DataFrame(tuple(row) for row in response_query_all)
        if len(response_query_all) == 1 and response_query_all[0][0] == '查詢成功':
            df.columns = [
                '查詢結果',
                '項次',
                '部門',
                '事件類型',
                '事件描述',
                '通知起始日',
                '週期',
                '假日除外',
                '郵件主旨',
                '郵件內容',
                '收件人',
                '建立時間',
                '規則終止日',
                '建立者',
                '修改者',
                '修改日期',
            ]
            for index, row in df.iterrows():
                try:
                    if not str(request.user
                               ) == row['建立者'] and not request.user.is_staff:
                        context['messages']['mail_test'] = '你只能測試自己建立的 Mail Job。'
                        return change_list(request, messages=context['messages'])
                except:
                    pass
    except:
        context['messages']['mail_test'] = '未知的錯誤，無法返回該筆資料。'
    if request.method == 'POST':
        try:
            # call do-test sp
            query_string = f"""
            exec mail_job.dbo.do_mail_job_onetime
            @seq_action='{seq}'
            ;
            """
            response_do_test = exec_sp(query_string=query_string)
            # end
        except:
            pass
        context['messages']['mail-test'] = '已經發出測試信。'
        return change_list(request, messages=context['messages'])
    else:
        return render(request, 'mail_job/mail_test.html', context)