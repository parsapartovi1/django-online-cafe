from django.contrib import admin

from .models import CafeWorkingHour, Category, Discount, Product, ProductSize, Table

# Register your models here.

admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(ProductSize)
admin.site.register(CafeWorkingHour)
