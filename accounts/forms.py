from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile, Department


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
    # the m2m formfields
    department = forms.ModelMultipleChoiceField(
        label=_('Dep.'),
        required=True,
        queryset=Department.objects.all(),
        help_text=_('The Departments you belong to. You could choose multiple ones with "ctrl + left-click".')
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
        instance.profile.department.set(self.cleaned_data['department'])
        instance.profile.save()
        return instance

class UserProfileForm(forms.ModelForm):

    phone_number = forms.CharField(
        label=_('Phone number'),
        max_length=32,
        required=False,
    )

    # the m2m formfields
    department = forms.ModelMultipleChoiceField(
        label=_('Dep.'),
        required=True,
        queryset=Department.objects.all(),
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
                self.fields['department'].initial = self.instance.profile.department.all()
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
        instance.profile.phone_number = self.cleaned_data['phone_number']
        instance.profile.department.set(self.cleaned_data['department'])
        instance.profile.save()
        return instance