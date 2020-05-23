from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
import pandas
from .forms import MailJobForm
from .mssql_sp import exec_sp
from django.utils.translation import gettext as _


def change_list(request, messages={}):
    print(request.LANGUAGE_CODE)
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
                'result', # 查詢結果
                _('Serial'), # 項次
                _('Dep.'), # 部門
                _('Event Type'), # 事件類型
                _('Event'), # 事件
                _('Start From'), # 通知起始日
                _('Period'), # 週期
                'weekend_flag', # 假日除外
                _('Mail Subject'), # 郵件主旨
                _('Mail Content'), # 郵件內容
                _('Recipients'), # 收件人
                _('Created Date'), # 建立時間
                'stop_date', # 規則終止日
                _('Created By'), # 建立者
                'update_by', # 修改者
                'update_date', # 修改日期
            ]
            for index, row in df.iterrows():
                items = [
                    f'<a class="dropdown-item" href="{reverse("mail_job:change", kwargs={"seq": row[_("Serial")]})}">{_("Change")}</a>',
                    f'<a class="dropdown-item" href="{reverse("mail_job:delete", kwargs={"seq": row[_("Serial")]})}">{_("Delete")}</a>',
                    f'<a class="dropdown-item" href="{reverse("mail_job:mail_test", kwargs={"seq": row[_("Serial")]})}">{_("Mail Test")}</a>',
                ]
                html_button_dropdown = '<div class="dropdown show">'
                html_button_dropdown += '<button class="btn btn-light bg-light dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                html_button_dropdown += _('Choose')
                html_button_dropdown += '</button>'
                html_button_dropdown += '<div class="dropdown-menu" aria-labelledby="dropdownMenuLink">'
                html_button_dropdown += f'{"".join(items)}'
                html_button_dropdown += '</div>'
                html_button_dropdown += '</div>'
                df.loc[index, _('Action')] = html_button_dropdown
                # merge the period and the weekend flag
                choices_period = [
                    ('單次', _('Once')),
                    ('每日', _('Daily')),
                    ('每日(假日除外)', _('Each weekday')),
                    ('每週一', _('Each Monday')),
                    ('每週二', _('Each Tuesday')),
                    ('每週三', _('Each Wednesday ')),
                    ('每週四', _('Each Thursday ')),
                    ('每週五', _('Each Friday ')),
                    ('每週六', _('Each Saturday ')),
                    ('每週日', _('Each Sunday')),
                    ('每月1號', _('1st of every month')),
                    ('每月2號', _('2nd of every month')),
                    ('每月3號', _('3rd of every month')),
                    ('每月4號', _('4th of every month')),
                    ('每月5號', _('5th of every month')),
                    ('每月6號', _('6th of every month')),
                    ('每月7號', _('7th of every month')),
                    ('每月8號', _('8th of every month')),
                    ('每月9號', _('9th of every month')),
                    ('每月10號', _('10th of every month')),
                    ('每月11號', _('11th of every month')),
                    ('每月12號', _('12th of every month')),
                    ('每月13號', _('13th of every month')),
                    ('每月14號', _('14th of every month')),
                    ('每月15號', _('15th of every month')),
                    ('每月16號', _('16th of every month')),
                    ('每月17號', _('17th of every month')),
                    ('每月18號', _('18th of every month')),
                    ('每月19號', _('19th of every month')),
                    ('每月20號', _('20th of every month')),
                    ('每月21號', _('21th of every month')),
                    ('每月22號', _('22th of every month')),
                    ('每月23號', _('23th of every month')),
                    ('每月24號', _('24th of every month')),
                    ('每月25號', _('25th of every month')),
                    ('每月26號', _('26th of every month')),
                    ('每月27號', _('27th of every month')),
                    ('每月28號', _('28th of every month')),
                    ('每月29號', _('29th of every month')),
                    ('每月30號', _('30th of every month')),
                    ('每月31號', _('31th of every month')),
                ]
                if row[_('Period')] == '每日' and row['weekend_flag'] == 'T':
                    df.loc[index, _('Period')] = _('Each weekday')
                else:
                    for t in choices_period:
                        if row[_('Period')] == t[0]:
                            df.loc[index, _('Period')] = t[1]
                if len(row[_('Mail Subject')]) > 50:
                    df.loc[index, _('Mail Subject')] = row[_('Mail Subject')][:50] + '......'
            df = df[[
                _('Action'), # 動作
                _('Dep.'), # 部門
                _('Event Type'), # 事件類型
                _('Event'), # 事件
                _('Start From'), # 通知起始日
                _('Period'), # 週期
                _('Mail Subject'), # 郵件主旨
                _('Mail Content'), # 郵件內容
                _('Recipients'), # 收件人
                _('Created By'), # 建立者
                _('Created Date'), # 建立時間
            ]]
            df = df.sort_values(by=[_('Created Date')], ascending=False)
            df.index = pandas.RangeIndex(start=1, stop=len(df) + 1, step=1)
            df_html = df.to_html(
                justify='left',
                classes=
                'j3y-df table table-light table-bordered table-striped table-responsive',
                escape=False,
            )
            context['htmls']['change_list'] = df_html
        else:
            context['messages']['change_list'] = '未知的錯誤，返回的資料格式不正確。'
    except Exception as e:
        print(e)
        context['messages']['change_list'] = '未知的錯誤，無法返回資料。'
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
        context['messages']['add'] = '輸入以下表格以新增 Mail Job。'
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
        'seq': seq,
        'messages': {},
        'form': None,
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