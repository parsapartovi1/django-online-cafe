from django.db import models
from user.models.py import User
# Create your models here.
#only payment transaction, discount and orders .
# orders ---> parsa

class Orders(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='user'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='product'
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Table reservation'
    )

    title = models.CharField(
        verbose_name='title',
        max_length=124
    )

    total_amount = models.DecimalField(
        verbose_name='total amount',
        decimal_places=2,
        max_digits=12
    )

    order_status = models.BooleanField(
        verbose_name='order status',
        default=False
    )

    cancellation = models.BooleanField(
        verbose_name='cancelation',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='create date',
        auto_now_add=True
    )

    update_date = models.DateTimeField(
        verbose_name='update date',
        auto_now=True
    )

    def __str__(self):
        return str(self.user) + " " + str(self.total_amount)

class Pay(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    status = models.BooleanField(
        verbose_name='status',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='create date',
        auto_now_add=True
    )

    update_date = models.DateTimeField(
        verbose_name='update date',
        auto_now=True
    )

    def __str__(self):
        return str(self.user)
