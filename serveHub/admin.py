from django.contrib import admin
from .models import Product,Category ,Discount , Table

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'final_price', 'created_date', 'last_update')
    list_filter = ('category', 'discount')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Discount)
