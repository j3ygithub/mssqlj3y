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
        if '@chief.com.tw' not in email:
            raise ValidationError(f'The Email address must contain "@chief.com.tw".')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'This Email has already been used.')
        return email


def sign_up_with_chief_email(request): 
    if request.method == 'POST': 
        form = ChiefUserSignUpForm(request.POST) 
        if form.is_valid():
            chief_user = form.save(commit=False)
            chief_email = form.cleaned_data.get('email')
            chief_user.username = chief_email[0:chief_email.index('@')]
            random_uuid_password = uuid.uuid4().hex[0:6]
            chief_user.set_password(random_uuid_password)
            chief_user.save()
            # send a random uuid password email
            recipient = f'{chief_email}'
            subject = '您在 Mail Job 上建立了一個新帳號'
            message = f'Hi {chief_user.username},\n\n您在 Mail Job 上註冊了一個新帳號，您的密碼是 {random_uuid_password}，您可以稍後在 Mail Job 上登入並更改這個密碼。\n\nMail Job'
            send_password_email(
                subject=subject,
                message=message,
                recipient=recipient,
            )
            return redirect('/accounts/password_reset/done/')
    else: 
        form = ChiefUserSignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up_with_chief_email.html', context) 

# a email-sending script, not a view
def send_password_email(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except:
        pass

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
