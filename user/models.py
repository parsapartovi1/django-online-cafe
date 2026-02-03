from django.db import models
from django.db.models import BooleanField


# Create your models here.

#user, comment
#comment --> alireza


class User(models.Model):
    first_name = models.CharField(
        max_length=24,
        verbose_name='first name',
        help_text='Enter your first name',
        blank=False,
        null = False
    )

    last_name = models.CharField(
        max_length=24,
        verbose_name='last name',
        help_text='Enter your last name',
        blank=False,
        null = False
    )

    number = models.CharField(
        max_length=11,
        verbose_name='number',
        help_text='Enter your number',
        blank=False,
        null = False
    )

    password= models.CharField(
        max_length=24,
        verbose_name='password',
        help_text='Enter your password',
        blank=False,
        null = False
    )

    user_rate= models.FloatField(
        verbose_name='user rate',
    )

    is_staff = models.BooleanField(
        verbose_name='staff status',
        default = False
    )

    user_presence = BooleanField(
        verbose_name='user presence',
        default = False
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now=True
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )
