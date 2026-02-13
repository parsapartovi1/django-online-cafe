from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Product name",
        help_text="enter product name",
        blank=False,
        null=False
    )

    image = models.ImageField(
        verbose_name="Product Image",
        help_text="upload product image",
        upload_to='products/',
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
        help_text="enter price in toman",
        blank=False,
        null=False
    )

    product_rate = models.FloatField(
        default=0.0,
        verbose_name="Product rating",
        help_text="average rating of the product"
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name="Category",
        help_text="select product category"
    )

    quantity = models.IntegerField(
        verbose_name="Quantity",
        help_text="Quantity of product",
        validators=[MinValueValidator(1) , MaxValueValidator(20)],
        default= 1
    )

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Discount",
        help_text="select discount if available"
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="create date"
    )

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="last update"
    )


    class Meta:
        verbose_name = "2. Product"
    def __str__(self):
        return self.name

    def final_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount.amount) / 100
            return self.price - discount_amount
        return self.price


class Table(models.Model):
    table_number = models.IntegerField(
        verbose_name="Table number",
        help_text="Specific Number of Table"
    )

    capacity = models.IntegerField(
        verbose_name="Capacity",
        help_text="Capacity of table"
    )

    duration = models.TimeField(
        verbose_name="Duration",
        help_text="Duration of table usage"
    )

    price = models.IntegerField(
        verbose_name="Price",
        help_text="Price of a Table"
    )

    create_date = models.DateTimeField(
        verbose_name="Create Date",
        help_text="Create date of a table",
        auto_now_add=True
    )

    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="last table record update",
        auto_now=True
    )

    class Meta:
        verbose_name = "1. Table"

    def __str__(self):
        return f"{self.table_number}"



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
        help_text="Create date of discount record",
        auto_now_add=True   
    )

    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of discount record Last Update",
        auto_now=True       
    )

    class Meta:
        verbose_name = "4. Discount"
    def __str__(self):
        return f"{self.amount} % for {self.duration}"



class Category(models.Model):
    type = models.CharField(
        max_length=30,
        verbose_name="Type",
        help_text="Type of Product"
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Description of Category"
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="category_discount"
    )

    create_date = models.DateTimeField(
        verbose_name="Create Date",
        help_text="Create date of Category",
        auto_now_add=True
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of Category Last Update",
        auto_now=True
    )
    class Meta:
        verbose_name = "3. Category"

    def __str__(self):
        return f"{self.type}"
