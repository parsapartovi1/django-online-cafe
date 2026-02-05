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
        help_text="Create date of discount record",
        auto_now=True
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of discount record Last Update",
        auto_now_add=True
    )

<<<<<<< HEAD

class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Product name",
        help_text="enter product name",
        blank=False,
        null=False
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
    
    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Discount",
        help_text="select discount if available"
    )
    
    created_date= models.DateTimeField(
        auto_now_add=True,
        verbose_name="create date"
    )
    
    last_update= models.DateTimeField(
        auto_now=True,
        verbose_name="last update"
    )

    def __str__(self):
        return self.name

    def final_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount.amount) / 100
            return self.price - discount_amount
        return self.price
=======
    def __str__(self):
        return f"{self.amount}"


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
        help_text="Create date of Category",
        auto_now=True
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="Date of Category Last Update",
        auto_now_add=True
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, related_name="category_discount"
    )

    def __str__(self):
        return f"{self.type}"
    
class Table(models.Model):
    table_number = models.IntegerField(
        verbose_name="Table number",
        help_text="Specific Number of Table"
    )
    capacity = models.IntegerField(
        verbose_name="Capacity",
        help_text="Capacity of tabel"
    )
    duration = models.TimeField(
        verbose_name="Duration",
        help_text="Duration of tabel usage"
    )
    price = models.IntegerField(
        verbose_name="Price",
        help_text="Price of a Table"
    )
    create_date = models.DateTimeField(
        verbose_name="Create Date",
        help_text="Create date of a table",
        auto_now=True
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        help_text="last table record update",
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.table_number}"
>>>>>>> origin/developer
