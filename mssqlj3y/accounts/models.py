from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name=_('User'),
        to=User,
        on_delete=models.CASCADE,
    )

    department = models.CharField(
        verbose_name=_('Dep.'),
        max_length=64,
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name=_('Phone number'),
        max_length=32,
        blank=True,
    )
