from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    
    user = models.OneToOneField(
        verbose_name=_('User'),
        to=User,
        on_delete=models.CASCADE,
    )

    department = models.ManyToManyField(
        to='Department',
        max_length=64,
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name=_('Phone number'),
        max_length=32,
        blank=True,
    )

class Department(models.Model):
    
    name = models.CharField(
        verbose_name=_('Name'),
        blank=True,
        max_length=32,
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        blank=True,
    )

    def __str__(self):
        return self.name
