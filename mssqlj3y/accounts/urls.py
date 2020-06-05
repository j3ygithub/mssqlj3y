from django.urls import path
from django.views.generic import RedirectView
from .views import sign_up, sign_up_with_account_password, sign_up_with_chief_email, send_password_email


urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-up/with-account-password/', sign_up_with_account_password, name='sign_up_with_account_password'), # not shown directly on web interface
    path('sign-up/with-chief-email/', sign_up_with_chief_email, name='sign_up_with_chief_email'),
    path('send-password-email/', send_password_email, name='send_password_email'),
]
