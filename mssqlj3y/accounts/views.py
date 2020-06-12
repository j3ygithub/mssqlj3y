from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid
from .forms import ChiefUserSignUpForm, UserProfileForm


def profile_change(request):
    """
    A profile change view.
    """
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    instance = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('Changed successfully.'))
            return redirect(reverse('profile_change'))
    else:
        form = UserProfileForm(instance=instance)
    context = {
        'form': form,
    }
    return render(request, 'registration/profile_change.html', context)

def set_role(request, role):
    """
    A set role view.
    """
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    if role not in [ dep.name for dep in request.user.profile.department.all() ]:
        messages.add_message(request, messages.ERROR, _('You have no access to this role.'))
        return redirect(reverse('index'))
    request.session['role'] = role
    return redirect(reverse('index'))

def sign_up(request):
    """
    A lobby view of sign-up view.
    """
    context = {}
    return render(request, 'registration/sign_up.html', context)

def sign_up_with_account_password(request):
    """
    A standard sign-up view.
    """
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

def get_name_dict(username):
    """
    For a given username string, generating a dictionary contaning
    first_name and last_name.
    """
    name_list = [ word[0:1].upper() + word[1:] for word in username.split('_') ]
    name_dict = {
        'first_name': ' '.join(name_list[0:1]),
        'last_name': ' '.join(name_list[1:]),
    }
    return name_dict

def sign_up_with_chief_email(request): 
    """
    A sign-up view for chief user.
    An user provides a Email and we use its prefix as username
    and generate a random uuid string as password.
    We then send a Email containing these info to users.
    """
    if request.method == 'POST': 
        form = ChiefUserSignUpForm(request.POST) 
        if form.is_valid():
            # Create a user and save it to DB.
            email = form.cleaned_data.get('email')
            username = email[0:email.index('@')]
            user = form.save(commit=False)
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]                
            user.set_password(random_uuid_password)
            user.first_name = get_name_dict(username)['first_name']
            user.last_name = get_name_dict(username)['last_name']
            user.save()
            # Send a login info Email.
            subject = '[Reminder] You have created an account.'
            message = (
                f'Hi {user.first_name} {user.last_name},\n'
                '\n'
                'You have created a new account on Reminder. You could login and change it on Reminder later.\n'
                '\n'
                f'Your account: {username}\n'
                f'Your password: {random_uuid_password}\n'
                '\n'
                'Sincerely,\n'
                'Reminder\n'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            department_emails = [ dep.email for dep in user.profile.department.all() ]
            # Send notification to departments the user joined.
            subject = f'[Reminder] {user.first_name} {user.last_name} has joined the group of you on Reminder.'
            message = (
                f'Hi there,\n'
                '\n'
                f'{user.first_name} {user.last_name} has joined the group of you on Reminder.\n'
                '\n'
                'Sincerely,\n'
                'Reminder\n'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=department_emails,
                fail_silently=False,
            )
            return redirect(reverse('password_reset_done'))
    else: 
        form = ChiefUserSignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up_with_chief_email.html', context) 
