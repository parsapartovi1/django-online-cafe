from django.db import models

class Product(models.Model):
    image = models.ImageField(
        verbose_name="Product Image",
        help_text="Upload product image",
        upload_to='serveHub/media/products_img',
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=50,
        verbose_name="Product Name",
        help_text="Enter product name",
        blank=False,
        null=False
    )

    size = models.CharField(
        max_length=50,
        verbose_name="Size / Type",
        help_text="e.g., single, double, small, medium, large",
        default="single"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Price (Toman)",
        help_text="Price in Toman",
        default=0.0
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
        help_text="Ingredients",
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
        return f"{self.name} - {self.size}"


class Table(models.Model):
    image = models.ImageField(
        verbose_name="Table Image",
        upload_to='serveHub/media/tables',
        blank=True,
        null=True
    )

    TABLE_TYPES = [
        ('single', 'میز تک نفره'),         
        ('couple', 'میز دو نفره'),
        ('family_3', 'میز سه نفره'),
        ('family_4', 'میز چهار نفره'),
        ('family_6', 'میز شش نفره'),
        ('family_8', 'میز هشت نفره - خانوادگی'),
        ('birthday', 'میز دیزاین تولد '),
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

    duration = models.IntegerField(
        verbose_name="Duration (minutes)",
        help_text="e.g., 120 minutes",
        default=120
    )

    price_per_person = models.IntegerField(
        verbose_name="Price per Person (Toman)",
        help_text="Price per person in Toman"
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
    image=models.ImageField(
        verbose_name="Image",
        upload_to='serveHub/media/categories',
        blank=True,
    )

    type = models.CharField(
        max_length=30,
        verbose_name="Category Name",
        help_text="Hot drinks , cold drinks etc.",
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