from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ChiefUserSignUpForm(forms.ModelForm):

    email = forms.EmailField(
        label=_('Chief Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Chief Email'),
            },
        ),
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@chief.com.tw' not in email:
            raise ValidationError(_('The Email address must contain "@chief.com.tw".'))
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This Email has already been used.'))
        return email
