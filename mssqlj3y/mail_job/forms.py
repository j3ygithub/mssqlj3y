from django import forms
from django.utils.timezone import now
from django.contrib.admin.widgets import AdminDateWidget


class SetupForm(forms.Form):
    department = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='部門',
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
                'placeholder': 'ex. 憑證到期',
            },
        ),
        label='事件類型',
        initial='憑證到期',
    )
    event = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex. jimmylin.chief.net.tw 憑證到期',
            },
        ),
        label='事件描述',
        max_length=32,
    )
    note_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type':'date',
            },
        ),
        label='通知起始日',
        initial=now,
    )
    choices_period = [
        ('單次', '單次'),
        ('每日', '每日'),
        ('每日(假日除外)', '每日(假日除外)'),
        ('每週一', '每週一'),
        ('每週二', '每週二'),
        ('每週三', '每週三'),
        ('每週四', '每週四'),
        ('每週五', '每週五'),
        ('每週六', '每週六'),
        ('每週日', '每週日'),
    ]
    choices_period += [(f'每月{n}號', f'每月{n}號') for n in range(1, 32)]
    period = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='週期',
        choices=choices_period,
        initial='每日',
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex. jimmylin.chief.net.tw 憑證到期通知',
            },
        ),
        label='郵件主旨',
        max_length=64,
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex.\njimmylin.chief.net.tw 憑證將於 2020/06/06 到期，請辦理更換新憑證。',
            },
        ),
        label='郵件內容',
        max_length=256,
    )
    recipient = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex.\njimmy_lin@chief.com.tw;\nt32@chief.com.tw;\ncathy_sung@chief.com.tw;',
            },
        ),
        label='收件人',
        max_length=256,
    )
    followed_action = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='後續動作',
        choices=(
            ('立即發出一封測試信件', '立即發出一封測試信件'),
            ('不動作', '不動作'),
        ),
        initial='立即發出一封測試信件',
    )


class LookupForm(forms.Form):
    department = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='部門',
        choices=(
            ('all', '全部'),
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

