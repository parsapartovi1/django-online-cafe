from django.db import models

# Create your models here.

#
#______________ATTENTION________________
# tables , product, category for this app
# product + category --> maryam
#tables --> agha ibrahim


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