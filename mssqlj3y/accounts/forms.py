from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile


class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            msg = _('There is no user registered with this Email.')
            self.add_error('email', msg)
        return email

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

    choice_department = [
        ('', _('Choose Department')),
        ('D11', _('D11')),
        ('D21', _('D21')),
        ('D31', _('D31')),
        ('T00', _('T00')),
        ('T11', _('T11')),
        ('T21', _('T21')),
        ('T22', _('T22')),
        ('T31', _('T31')),
        ('T32', _('T32')),
    ]

    department = forms.CharField(
        widget=forms.Select(choices=choice_department),
        label=_('Dep.'),
        max_length=64,
        required=True,
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email[-13:] != '@chief.com.tw':
            self.add_error(
                'email',
                ValidationError(
                    _('The Email address must end with "@chief.com.tw".'),
                    code='invalid'
                )
            )   
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    _('The Email has already been used.'),
                    code='invalid'
                )
            )
        return email

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.save()
        if not Profile.objects.filter(user=self.instance.pk).exists():
            profile = Profile.objects.create(user=instance)
            profile.save()
        instance.profile.department = self.cleaned_data['department']
        instance.profile.save()
        return instance

class UserProfileForm(forms.ModelForm):

    # from reverse-one-to-one formfield
    choice_department = [
        ('', _('Choose')),
        ('D11', _('D11')),
        ('D21', _('D21')),
        ('D31', _('D31')),
        ('T00', _('T00')),
        ('T11', _('T11')),
        ('T21', _('T21')),
        ('T22', _('T22')),
        ('T31', _('T31')),
        ('T32', _('T32')),
    ]

    department = forms.CharField(
        widget=forms.Select(choices=choice_department),
        label=_('Dep.'),
        max_length=64,
        required=True,
    )

    phone_number = forms.CharField(
        label=_('Phone number'),
        max_length=32,
        required=False,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if Profile.objects.filter(user=self.instance.pk).exists():
                self.fields['email'].disabled = True
                self.fields['department'].disabled = True
                self.fields['department'].initial = self.instance.profile.department
                self.fields['phone_number'].initial = self.instance.profile.phone_number
            else:
                self.fields['email'].disabled = False
                self.fields['department'].disabled = False

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.save()
        if not Profile.objects.filter(user=self.instance.pk).exists():
            profile = Profile.objects.create(user=instance)
            profile.save()
        instance.profile.department = self.cleaned_data['department']
        instance.profile.phone_number = self.cleaned_data['phone_number']
        instance.profile.save()
        return instance