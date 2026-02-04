from django.db import models


class Discount(models.Model):
    amount = models.IntegerField(
        verbose_name="Amount",
        help_text="Amount of Discount"
    )
    duration = models.DateTimeField(
        verbose_name="Duration",
        help_text="Duration of Discount"
    )
    create_date = models.DateTimeField(
        verbose_name="Create Date",
        help_text="Create date of discount record"
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of discount record Last Update"
    )


class Category(models.Model):
    type = models.CharField(
        max_length=30,
        verbose_name="Type",
        help_text="Type of Product"
        )
    discription = models.TextField(
        verbose_name="Discription",
        help_text="Discription of Category"
    )
    create_date = models.DateTimeField(
        verbose_name="Create Date",
        help_text="Create date of Category"
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of Category Last Update"
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, related_name="category_discount"
    )
