from django.db import models

# Create your models here.

#
#______________ATTENTION________________
# tables , product, category for this app
# product + category --> maryam
#tables --> agha ibrahim


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_rate = models.FloatField(default=0.0) 
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def final_price(self):
        if self.discount:
            return self.price - (self.price * self.discount.amount / 100)
        return self.price