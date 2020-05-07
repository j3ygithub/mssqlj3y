from django import forms

class MailJobForm(forms.Form):
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
    event_class = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='類型',
        choices=(
            ('憑證到期', '憑證到期'),
            ('其他', '其他'),
        ),
    )
    event = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'im.chiefcall.com.tw憑證於2021/6/6到期通知',
            },
        ),
        label='事件',
        max_length=64,
    )
    note_date = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={
                'class': 'form-control'
            },
            empty_label=(
                'Choose Year', 'Choose Month', 'Choose Day'
            ),
        ),
        label='日期',
    )
    period = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='週期',
        choices=(
            ('每日', '每日'),
            ('每周一', '每周一'),
            ('每月1號', '每月1號'),
        ),
    )
    weekend_flag = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
        label='假日例外',
        choices=(
            ('T', '是'),
            ('F', '否'),
        ),
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'im.chiefcall.com.tw憑證於到期通知',
            },
        ),
        label='標題',
        max_length=64,
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'im.chiefcall.com.tw憑證將於2020/6/6到期，請辦理更換新憑證',
            },
        ),
        label='內容',
        max_length=256,
    )
    recipient = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'jimmy_lin@chief.com.tw;',
            },
        ),
        label='收件人',
    )
