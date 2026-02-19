from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Product Name",
        help_text="Enter product name",
        blank=False,
        null=False
    )

    image = models.ImageField(
        verbose_name="Product Image",
        help_text="Upload product image",
        upload_to='products_img/',
        blank=True,
        null=True
    )

    product_rate = models.FloatField(
        default=0.0,
        verbose_name="Product Rating",
        help_text="Average rating of the product"
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name="Category",
        help_text="Select product category"
    )

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Discount",
        help_text="Select discount if available"
    )

    description = models.TextField(
        verbose_name="Description / Ingredients",
        help_text="e.g., espresso, steamed milk",
        blank=True,
        null=True
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create Date"
    )

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Main Product",
        related_name='variants'
    )

    size = models.CharField(
        max_length=50,
        verbose_name="Size / Type",
        help_text="e.g., single, double, small, medium, large",
        blank=False,
        null=False
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Price (Toman)",
        help_text="Price in Toman",
        blank=False,
        null=False
    )

    quantity = models.IntegerField(
        verbose_name="Stock",
        help_text="Quantity available for this size",
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        default=1
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create Date"
    )

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Table(models.Model):
    TABLE_TYPES = [
        ('single', 'میز تک نفره'),         
        ('couple', 'میز دو نفره'),
        ('family_3', 'میز سه نفره'),
        ('family_4', 'میز چهار نفره'),
        ('family_6', 'میز شش نفره'),
        ('family_8', 'میز هشت نفره - خانوادگی'),
        ('birthday', 'میز تولد (ویژه)'),
        ('vip', 'میز VIP'),
    ]
    
    table_number = models.IntegerField(
        verbose_name="Table Number",
        help_text="Enter table number",
        unique=True
    )

    table_type = models.CharField(
        max_length=20,
        choices=TABLE_TYPES,
        verbose_name="Table Type",
        default='family_4'
    )

    capacity = models.IntegerField(
        verbose_name="Capacity",
        help_text="Number of persons"
    )

    duration = models.IntegerField(
        verbose_name="Duration (minutes)",
        help_text="e.g., 120 minutes",
        default=120
    )

    price_per_person = models.IntegerField(
        verbose_name="Price per Person (Toman)",
        help_text="Price per person in Toman"
    )

    image = models.ImageField(
        verbose_name="Table Image",
        upload_to='tables/',
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name="Description",
        help_text="Description about the table (e.g., suitable for birthday)",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        verbose_name="Available for Reservation",
        default=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create Date"
    )

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"Table {self.table_number} - {self.get_table_type_display()}"

    def total_price(self, people_count):
        """Calculate total price based on number of people"""
        return self.price_per_person * people_count


class Discount(models.Model):
    amount = models.IntegerField(
        verbose_name="Discount Percent",
        help_text="Enter discount amount"
    )

    duration = models.DateTimeField(
        verbose_name="Valid Until",
        help_text="Discount validity duration"
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create Date"
    )

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
    
    def __str__(self):
        return f"{self.amount}% until {self.duration}"


class Category(models.Model):
    type = models.CharField(
        max_length=30,
        verbose_name="Category Type",
        help_text="e.g., Espresso, Hot Drink, etc"
    )
    
    description = models.TextField(
        verbose_name="Description",
        help_text="Category description",
        blank=True,
        null=True
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="category_discount",
        verbose_name="Category Discount"
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create Date"
    )
    
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.type