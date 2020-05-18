"""mssqlj3y URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import RedirectView
from .views import sign_up, send_password_email, sign_up_with_chief_email

urlpatterns = [
    # path('sign_up/', sign_up, name='sign_up'),
    path('send-password-email/', send_password_email, name='send_password_email'),
    path('sign-up/', RedirectView.as_view(url='/accounts/sign-up/with-chief-email/'), name='sign_up'),
    path('sign-up/with-chief-email/', sign_up_with_chief_email, name='sign_up_with_chief_email'),
]
