from django.urls import path, include
from django.views.generic import RedirectView
from .views import change_list, add, change, delete, mail_test


app_name = 'mail_job'

urlpatterns = [
    path('', change_list, name='change_list'),
    path('add/', add, name='add'),
    path('<int:seq>/change/', change, name='change'),
    path('<int:seq>/delete/', delete, name='delete'),
    path('<int:seq>/mail-test/', mail_test, name='mail_test'),
]
