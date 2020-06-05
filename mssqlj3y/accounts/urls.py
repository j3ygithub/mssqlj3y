from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.utils.translation import gettext_lazy as _
from .views import sign_up, sign_up_with_account_password, sign_up_with_chief_email, send_password_email
from .forms import EmailValidationOnForgotPassword


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'password-reset/',
        PasswordResetView.as_view(
            form_class=EmailValidationOnForgotPassword,
        ),
        name='password_reset'
    ),
    path(
        'password-reset-confirm/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    )
]

urlpatterns += [
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-up/with-account-password/', sign_up_with_account_password, name='sign_up_with_account_password'), # not shown directly on web interface
    path('sign-up/with-chief-email/', sign_up_with_chief_email, name='sign_up_with_chief_email'),
]
