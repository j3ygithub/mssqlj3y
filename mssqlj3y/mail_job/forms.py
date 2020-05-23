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
        label=_('Department'),
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
        label=_('Event Type'),
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
        label=_('Start From'),
        initial=today,
    )
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
    ]
    choices_period += [
        ('每月1號', _('1st of every month')),
    ]
    choices_period += [
        (f'每月{n}號',  _(f"{n}th of every month")) for n in range(1, 32)
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
        label=_('Mail Subject'),
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
        label=_('Mail Content'),
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
