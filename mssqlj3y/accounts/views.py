from django.shortcuts import HttpResponse, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import uuid

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ChiefUserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This Email already exists.')
        return email


def chief_user_sign_up(request): 
    if request.method == 'POST': 
        form = ChiefUserSignUpForm(request.POST) 
        if form.is_valid():
            chief_user = form.save(commit=False)
            chief_email = form.cleaned_data.get('email')
            chief_user.username = chief_email[0:chief_email.index('@')]
            chief_user.password = uuid.uuid4().hex[0:6]
            chief_user.save()
            return redirect('/')
    else: 
        form = ChiefUserSignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/chief_user_sign_up.html', context) 


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)


first_name = 'Jimmy'
last_name = 'Lin'
recipient = 'jimmy_lin@chief.com.tw'
subject = '您在 Mail Job 上註冊了一個新帳號'
message = f"""Hi {first_name} {last_name},

您在 Mail Job 上註冊了一個新帳號，您的密碼是 1b386d，稍後您可以在 Mail Job 上登入並更改這個密碼。

Mail Job
"""
from_email = settings.EMAIL_HOST_USER

def send_email(request):
    response = send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
        fail_silently=False,
    )
    try:
        if response == 1:
            return HttpResponse(f'Email has been sent to {recipient} successfully!')
    except:
        pass
    return HttpResponse(f'Fail. Email has not been sent.')
