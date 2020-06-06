from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .forms import ChiefUserSignUpForm, UserProfileForm


def profile_change(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    instance = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('Changed successfully.'))
            redirect(reverse('profile_change'))
    else:
        form = UserProfileForm(instance=instance)
    context = {
        'form': form,
    }
    return render(request, 'registration/profile_change.html', context)

def sign_up(request):
    context = {}
    return render(request, 'registration/sign_up.html', context)

def sign_up_with_account_password(request):
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
    return render(request, 'registration/sign_up_with_account_password.html', context)

def sign_up_with_chief_email(request): 
    if request.method == 'POST': 
        form = ChiefUserSignUpForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = email[0:email.index('@')]
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]
            user.set_password(random_uuid_password)
            user.save()
            # send a random uuid password email
            recipient = f'{email}'
            subject = "[Mail Job] You have created an account."
            try:
                if '_' in username:
                    username_readable = ' '.join([ word[0].upper() + word[1:] for word in username.split('_') ])
                else:
                    username_readable = username
            except:
                username_readable = username
            message = f'Hi {username_readable},'
            message += '\n\nYou have created a new account on Mail Job. You could login and change it on Mail Job later.'
            message += f'\n\nYour account: {username}'
            message += f'\nYour password: {random_uuid_password}'
            message += '\n\nSincerely,'
            message += '\nMail Job'
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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except:
        pass
