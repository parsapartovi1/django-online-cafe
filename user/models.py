from django.db import models
from serveHub.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import WeekDays

class User(models.Model):
    first_name = models.CharField(
        max_length=24,
        verbose_name='first name',
        help_text='Enter your first name',
        blank=False,
        null=False
    )

    last_name = models.CharField(
        max_length=24,
        verbose_name='last name',
        help_text='Enter your last name',
        blank=False,
        null=False
    )

    number = models.CharField(
        max_length=11,
        verbose_name='number',
        help_text='Enter your number',
        blank=False,
        null=False
    )

    password = models.CharField(
        max_length=24,
        verbose_name='password',
        help_text='Enter your password',
        blank=False,
        null=False
    )

    user_rate = models.FloatField(
        verbose_name='user rate',
        default=0
    )

    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False
    )

    user_presence = models.BooleanField(
        verbose_name='user presence',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True  
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )
    class Meta:
        verbose_name = "1. user"
    def __str__(self):
        return f"{self.first_name} + {self.last_name}"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        help_text='Select the user who wrote the comment'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='product',
        help_text='Select the product related to this comment'
    )

    text = models.TextField(
        verbose_name='comment text',
        help_text='Enter your comment text',
        blank=False,
        null=False
    )

    com_rate = models.FloatField(
        verbose_name='comment rate',
        help_text='Rate the product from 1 to 5',
        default=0,
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )

    delete = models.BooleanField(
        verbose_name='deleted status',
        help_text='Mark if the comment is deleted',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )

    class Meta:
        verbose_name = "2. comment"

    def __str__(self):
        return f"{self.user.first_name}" + "about" + "{self.product.name}"


class Reply(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
    )

    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='comment',
    )

    text = models.TextField(
        verbose_name='reply text',
        help_text='Enter your reply text'
    )

    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )
    class Meta:
        verbose_name = "3. Reply"

    def __str__(self):
        return f"{self.user.first_name}"



class WorkingShift(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    weekdays = models.CharField(
            max_length=24,
            choices=WeekDays.choices,
            verbose_name='weekday',
    )

    opening_date = models.DateField(
        verbose_name='opening date',
        help_text='Enter your opening date'
    )

    closed_date = models.DateField(
        verbose_name='closed date',
        help_text='Enter your close date'
    )

    class Meta:
        verbose_name = "4. Working Shift"

    def __str__(self):
        return str(self.weekdays) + "-" + str(self.opening_date) + "-" + str(self.closed_date)
