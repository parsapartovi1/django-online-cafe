from django.db import models
from serveHub.models import Product  

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
        auto_now_add=True   # اصلاح شد
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    com_rate = models.PositiveSmallIntegerField()
    delete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} → {self.product.name}: {self.text[:30]}"
