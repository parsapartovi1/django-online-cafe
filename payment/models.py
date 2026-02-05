from django.db import models

# Create your models here.
#only payment transaction, discount and orders .
# orders ---> parsa
from django.db import models
# Create your models here.
from user.models import User
from serveHub.models import Product
from serveHub.models import Table


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='product'
    )

    table=models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Table'
    )

    title= models.CharField(
        verbose_name='title',
        max_length=100,
        default=''
    )

    total_amount = models.FloatField(
        verbose_name='total amount',
        default=0.0
    )

    order_status = models.BooleanField(
        verbose_name='status',
        default=False
    )

    cancellation = models.BooleanField(
        verbose_name='cancellation',
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

    class Meta:
        verbose_name = "1. Order"

    def __str__(self):
        return str(self.user) + " " + str(self.total_amount) +  str(self.order_status)

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

    class Meta:
        verbose_name = "2. Pay"

    def __str__(self):
        return str(self.user)