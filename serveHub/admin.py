from django.contrib import admin
from .models import Product, Category, Discount, Table, ProductVariant

# Register your models here.

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    verbose_name = "نوع محصول"
    verbose_name_plural = "انواع محصول"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_rate', 'created_date', 'last_update')
    list_filter = ('category', 'discount')
    search_fields = ('name', 'name_en')
    inlines = [ProductVariantInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Discount)