from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib import messages
import pandas
from .mssql_sp import sp_show_mail_job, sp_show_mail_job_1, sp_insert_mail_job, sp_update_mail_job, sp_do_mail_job_onetime
from .forms import MailJobForm


def change_list_new(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
        'jsons': None
    }
    try:
        response_show = sp_show_mail_job()
        dfs = pandas.DataFrame(tuple(row) for row in response_show)
        jsons = dfs.to_json(orient='records')
        print(jsons)
        context['jsons'] = jsons
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    return render(request, 'mail_job/change_list_new.html', context)

def change_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
        'htmls': {},
    }
    try:
        response_show = sp_show_mail_job()
        if response_show[0][0] == '查詢成功':
            df = pandas.DataFrame(tuple(row) for row in response_show)
            df.columns = [
                'result', # 查詢結果
                _('Serial'), # 項次
                _('Dep.'), # 部門
                _('Event type'), # 事件類型
                _('Event'), # 事件
                _('Start from'), # 通知起始日
                _('Period'), # 週期
                'weekend_flag', # 假日除外
                _('Mail subject'), # 郵件主旨
                _('Mail content'), # 郵件內容
                _('Recipients'), # 收件人
                _('Created date'), # 建立時間
                'stop_date', # 規則終止日
                _('Created by'), # 建立者
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
                    ('平日', _('Each weekday')),
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
                if len(row[_('Mail content')]) > 50:
                    df.loc[index, _('Mail content')] = row[_('Mail content')][:50] + '......'
            df = df[[
                _('Action'), # 動作
                _('Dep.'), # 部門
                _('Event type'), # 事件類型
                _('Event'), # 事件
                _('Start from'), # 通知起始日
                _('Period'), # 週期
                _('Mail subject'), # 郵件主旨
                _('Mail content'), # 郵件內容
                _('Recipients'), # 收件人
                _('Created by'), # 建立者
                _('Created date'), # 建立時間
            ]]
            df = df.sort_values(by=[_('Created date')], ascending=False)
            df.index = pandas.RangeIndex(start=1, stop=len(df) + 1, step=1)
            df_html = df.to_html(
                justify='left',
                classes=
                'j3y-df table table-light table-bordered table-striped table-responsive',
                escape=False,
            )
            context['htmls']['change_list'] = df_html
        else:
            context['tips'] += [_('Unknown error. The format of the returned data is not correct.')]
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    return render(request, 'mail_job/change_list.html', context)


def add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
        'form': None,
    }
    if request.method != 'POST':
        form = MailJobForm()
        context['tips'] += [_('Fill in the following form to create a new mail job.')]
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
            if period == '平日':
                period = '每日'
                weekend_flag = 'T'
            else:
                weekend_flag = 'F'
        try:
            response_insert = sp_insert_mail_job(
                department=department,
                event_class=event_class,
                event=event,
                note_date=note_date,
                period=period,
                weekend_flag=weekend_flag,
                subject=subject,
                body=body,
                recipient=recipient,
                created_by=created_by,
            )
            if response_insert[0][0] == '新增成功':
                messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
                return redirect(reverse('mail_job:change_list'))
            elif response_insert[0][0] == '新增失敗，資料重覆，請確認':
                messages.add_message(request, messages.ERROR, _('Failed to add. The data is duplicate with the existing.'))
            else:
                messages.add_message(request, messages.ERROR, _('Unknown error. The format of the return value is not correct.'))
        except:
            context['tips'] += [_('Unknown error. The format of the return value is not correct.')]
        return render(request, 'mail_job/add.html', context)


def change(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
        'seq': seq,
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
            updated_by = request.user
            if period == '平日':
                period = '每日'
                weekend_flag = 'T'
            else:
                weekend_flag = 'F'
        try:
            response_update = sp_update_mail_job(
                seq=seq,
                department=department,
                event_class=event_class,
                event=event,
                note_date=note_date,
                period=period,
                weekend_flag=weekend_flag,
                subject=subject,
                body=body,
                recipient=recipient,
                updated_by=updated_by,
            )
            print(response_update)
            if response_update[0][0] == '修改成功':
                messages.add_message(request, messages.SUCCESS, _('Changed successfully.'))
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, _('Unknown error. The format of the return value is not correct.'))
        return redirect(reverse('mail_job:change_list'))
    else:
        try:
            response_show = sp_show_mail_job(seq=seq)
        except:
            messages.add_message(request, messages.ERROR, _('Unknown error. The data cannot be returned.'))
        try:
            df = pandas.DataFrame(tuple(row) for row in response_show)
            if len(response_show
                   ) == 1 and response_show[0][0] == '查詢成功':
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
                            messages.add_message(request, messages.ERROR, _('You can only change the mail job created by you.'))
                            return redirect(reverse('mail_job:change_list'))
                    except:
                        pass
                    if row['週期'] == '每日' and row['假日除外'] == 'T':
                        df.loc[index, '週期'] = '平日'
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
                context['tips'] += [_('The following is the current setting. Please fill in the part you want to modify and then submit.')]
            else:
                context['tips'] += [_('The mail job is not available. Please confirm whether it has been deleted.')]
        except:
            context['tips'] += [_('Unknown error, data cannot return.')]
        return render(request, 'mail_job/change.html', context)


def delete(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
        'messages': {},
    }
    try:
        response_show = sp_show_mail_job(seq=seq)
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    try:
        df = pandas.DataFrame(tuple(row) for row in response_show)
        if len(response_show) == 1 and response_show[0][0] == '查詢成功':
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
                        messages.add_message(request, messages.ERROR, _('You can only delete the mail job created by you.'))
                        return redirect(reverse('mail_job:change_list'))
                except:
                    pass
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    if request.method == 'POST':
        updated_by = request.user
        try:
            response_update = sp_update_mail_job(
                seq=seq,
                stop_date=timezone.localtime(timezone.now()).date(),
                updated_by=updated_by,
            )
            if response_update[0][0] == '修改成功':
                messages.add_message(request, messages.SUCCESS, _('Deleted successfully.'))
            else:
                messages.add_message(request, messages.ERROR, _('The mail job is not available. Please confirm whether it has been deleted.'))            
        except:
            context['messages']['delete'] = _('Unknown error, data cannot return.')
        return redirect(reverse('mail_job:change_list'))
    else:
        return render(request, 'mail_job/delete.html', context)


def mail_test(request, seq):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'tips': [],
    }
    try:
        response_show = sp_show_mail_job(seq=seq)
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    try:
        df = pandas.DataFrame(tuple(row) for row in response_show)
        if len(response_show) == 1 and response_show[0][0] == '查詢成功':
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
                        messages.add_message(request, messages.ERROR, _('You can only do a mail test on the mail job created by you.'))
                        return redirect(reverse('mail_job:change_list'))
                except:
                    pass
    except:
        context['tips'] += [_('Unknown error. The data cannot be returned.')]
    if request.method == 'POST':
        try:
            response_do_test = sp_do_mail_job_onetime(seq=seq)
        except:
            pass
        messages.add_message(request, messages.SUCCESS, _('The test mail has been sent.'))
        return redirect(reverse('mail_job:change_list'))
    else:
        return render(request, 'mail_job/mail_test.html', context)