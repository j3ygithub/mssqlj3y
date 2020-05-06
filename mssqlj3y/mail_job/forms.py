from django import forms

class MailJobForm(forms.Form):
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Department',
        max_length=64,
    )
    event = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Event',
        max_length=256,
    )
