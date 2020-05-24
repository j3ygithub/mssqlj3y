from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def today():
    return timezone.localtime(timezone.now()).date()


class MailJobForm(forms.Form):
    department = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label=_('Dep.'),
        choices=(
            ('D11', 'D11'),
            ('D21', 'D21'),
            ('D31', 'D31'),
            ('T11', 'T11'),
            ('T12', 'T12'),
            ('T21', 'T21'),
            ('T22', 'T22'),
            ('T31', 'T31'),
            ('T32', 'T32'),
        ),
    )
    event_class = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('ex. Expiration of certificates'),
            },
        ),
        label=_('Event type'),
        max_length=32,
    )
    event = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('ex. Expiration of the certificate on jimmylin.chief.net.tw'),
                'rows':2,
            },
        ),
        label=_('Event'),
        max_length=32,
    )
    note_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type':'date',
            },
        ),
        label=_('Start on'),
        initial=today,
    )
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
    period = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label=_('Period'),
        choices=choices_period,
        initial='每日',
    )
    subject = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('ex. Notification - Certificate Expiration - jimmylin.chief.net.tw'),
                'rows':2,
            },
        ),
        label=_('Mail subject'),
        max_length=64,
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('ex.\nThe Certificate on jimmylin.chief.net.tw will expire on 2020/06/06. Please update it.'),
                'rows':16,
            },
        ),
        label=_('Mail content'),
        max_length=512,
    )
    recipient = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('ex.\njimmy_lin@chief.com.tw;\nt32@chief.com.tw;\ncathy_sung@chief.com.tw;'),
                'rows':8,
            },
        ),
        label=_('Recipients'),
        max_length=256,
    )
