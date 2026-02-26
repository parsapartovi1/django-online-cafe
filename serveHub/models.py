from django.db import models
from django.utils import timezone
from decimal import Decimal



class ProductSize(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default=''
    )

    size1 = models.CharField(
        max_length=30,
        help_text="Size according to the product",
    )

    price1 = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    size2=models.CharField(
        max_length=30,
        help_text="other Size according to the product",
        blank=True,
        null=True
    )
    price2 = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True

    )
    size3=models.CharField(
        max_length=30,
        help_text="other Size according to the product",
        blank=True,
        null=True
    )
    price3 = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True
    )

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    @property
    def has_active_discount(self):
        return (
                self.discount and
                self.discount.duration > timezone.now()
        )

    def get_final_price1(self):
        if self.discount and self.discount.duration > timezone.now():
            return int(self.price1 - (self.price1 * self.discount.amount / 100))
        return int(self.price1)

    def get_final_price2(self):
        if self.price2 and self.has_active_discount:
            return int(self.price2 - (self.price2 * self.discount.amount / 100))
        return int(self.price2) if self.price2 else 0

    def get_final_price3(self):
        if self.price3 and self.discount and self.discount.duration > timezone.now():
            return int(self.price3 - (self.price3 * self.discount.amount / 100))
        return int(self.price3) if self.price3 else 0

    def get_discount_percent(self):
        if self.discount and self.discount.duration > timezone.now():
            return self.discount.amount
        return 0

    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )

    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "ProductSize"

    def __str__(self):
        return f"{self.name} - sizes"



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

    size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        verbose_name="Product Size",
        help_text="Select product size",
        blank=True,
        null=True,
        related_name="main_product"
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
        related_name="product_discount",
        verbose_name="Product Discount",
    )


    description = models.TextField(
        verbose_name="Description / Ingredients",
        help_text="Ingredients",
        blank=True,
        null=True
    )


    def get_average_rating(self):
        comments = self.comment_set.filter(is_delete=False)
        if comments.exists():
            return round(sum(c.com_rate for c in comments) / comments.count(), 1)
        return 0.0


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

    def get_active_discount_percent(self):
        now = timezone.now()
        candidates = []

        if self.size and self.size.discount and self.size.discount.duration > now:
            candidates.append(self.size.discount.amount)
        if self.discount and self.discount.duration > now:
            candidates.append(self.discount.amount)
        if self.category.discount and self.category.discount.duration > now:
            candidates.append(self.category.discount.amount)

        return max(candidates) if candidates else 0

    def get_price_for_size(self, size_key=1):
        if not self.size:
            return 0

        price_map = {
            1: self.size.price1,
            2: self.size.price2,
            3: self.size.price3,
        }
        raw_price = price_map.get(size_key)
        if raw_price is None:
            return 0

        discount_percent = self.get_active_discount_percent()
        final_price = Decimal(raw_price) * (Decimal(100) - Decimal(discount_percent)) / Decimal(100)
        return int(final_price)

    def get_price_size1(self):
        return self.get_price_for_size(1)

    def get_price_size2(self):
        return self.get_price_for_size(2)

    def get_price_size3(self):
        return self.get_price_for_size(3)

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

    capacity = models.IntegerField(
        help_text='Number of persons',
        verbose_name='Capacity',
        default=1,
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


class CafeWorkingHour(models.Model):
    WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        unique=True,
        verbose_name="Weekday",
    )
    opens_at = models.TimeField(verbose_name="Opens At")
    closes_at = models.TimeField(verbose_name="Closes At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Cafe Working Hour"
        verbose_name_plural = "Cafe Working Hours"
        ordering = ["weekday"]

    def __str__(self):
        return f"{self.get_weekday_display()} ({self.opens_at}-{self.closes_at})"


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
