from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from serveHub.models import Product

from .choices import WeekDays


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, number, email, password=None, **extra_fields):
        if not number:
            raise ValueError("The number must be set.")
        if not email:
            raise ValueError("The email must be set.")

        user = self.model(
            number=str(number),
            email=self.normalize_email(email),
            **extra_fields,
        )
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(number, email, password, **extra_fields)

    def create_superuser(self, number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(number, email, password, **extra_fields)


class User(AbstractUser):
    username = None

    first_name = models.CharField(
        max_length=24,
        verbose_name="first name",
        help_text="Enter your first name",
        blank=True,
        default="",
    )

    last_name = models.CharField(
        max_length=24,
        verbose_name="last name",
        help_text="Enter your last name",
        blank=True,
        default="",
    )

    email = models.EmailField(
        verbose_name="email address",
        help_text="Enter your email",
    )

    number = models.CharField(
        max_length=11,
        verbose_name="number",
        help_text="Enter your number",
        unique=True,
    )

    user_rate = models.FloatField(
        verbose_name="user rate",
        default=0,
    )

    user_presence = models.BooleanField(
        verbose_name="user presence",
        default=False,
    )

    create_date = models.DateTimeField(
        verbose_name="creation date",
        auto_now_add=True,
    )

    last_update = models.DateTimeField(
        verbose_name="last update",
        auto_now=True,
    )

    USERNAME_FIELD = "number"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "1. user"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.number


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user',
        help_text='Select the user who wrote the comment'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='product',
        help_text='Select the product related to this comment'
    )

    reservation = models.ForeignKey(
        'payment.Reservation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments',
        verbose_name='reservation',
    )

    text = models.TextField(
        verbose_name='comment text',
        help_text='Enter your comment text',
        blank=False,
        null=False
    )

    com_rate = models.FloatField(
        verbose_name='comment rate',
        help_text='Rate the product from 1 to 5',
        default=0,
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )

    is_delete = models.BooleanField(
        verbose_name='deleted status',
        help_text='Mark if the comment is deleted',
        default=False
    )

    is_locked = models.BooleanField(
        verbose_name='comment locked',
        default=False,
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )

    class Meta:
        verbose_name = "2. comment"

    def __str__(self):
        return f"{self.user.first_name}  about  {self.product.name}"


class Reply(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user',
    )

    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='comment',
    )

    text = models.TextField(
        verbose_name='reply text',
        help_text='Enter your reply text'
    )

    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )

    last_update = models.DateTimeField(
        verbose_name='last update',
        auto_now=True
    )
    class Meta:
        verbose_name = "3. Reply"

    def __str__(self):
        return f"{self.user.first_name} to {self.comment.user.first_name}"

class WorkingShift(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    weekdays = models.CharField(
        max_length=24,
        choices=WeekDays.choices,
        verbose_name='weekday',
    )

    opening_date = models.DateTimeField(
        verbose_name='opening date',
        help_text='Enter your opening date'
    )

    closed_date = models.DateTimeField(
        verbose_name='closed date',
        help_text='Enter your close date'
    )

    class Meta:
        verbose_name = "4. Working Shift"

    def __str__(self):
        return f"{self.weekdays} - {self.opening_date} - {self.closed_date}"
