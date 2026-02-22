from django.contrib import admin
from .models import Product, Category, Discount, Table

# Register your models here.

admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Discount)