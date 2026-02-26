from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from serveHub.models import Product
from serveHub.models import Table


# Create your models here.






class Reservation(models.Model):
    STATUS_RESERVED = "reserved"
    STATUS_CANCELLED_BY_USER = "cancelled_by_user"
    STATUS_CANCELLED_BY_MANAGER = "cancelled_by_manager"
    STATUS_CHOICES = [
        (STATUS_RESERVED, "Reserved"),
        (STATUS_CANCELLED_BY_USER, "Cancelled by user"),
        (STATUS_CANCELLED_BY_MANAGER, "Cancelled by manager"),
    ]

    ATTENDANCE_PENDING = "pending"
    ATTENDANCE_PRESENT = "present"
    ATTENDANCE_ABSENT = "absent"
    ATTENDANCE_CHOICES = [
        (ATTENDANCE_PENDING, "Pending"),
        (ATTENDANCE_PRESENT, "Present"),
        (ATTENDANCE_ABSENT, "Absent"),
    ]

    DECISION_PENDING = "pending"
    DECISION_APPROVED = "approved"
    DECISION_REJECTED = "rejected"
    DECISION_CHOICES = [
        (DECISION_PENDING, "Pending"),
        (DECISION_APPROVED, "Approved"),
        (DECISION_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="user",
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="table",
    )
    start_time = models.DateTimeField(verbose_name="reservation start")
    end_time = models.DateTimeField(verbose_name="reservation end")
    people_count = models.PositiveIntegerField(verbose_name="people count")
    table_unit_price = models.PositiveIntegerField(verbose_name="table unit price")

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_RESERVED,
        verbose_name="reservation status",
    )
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancelled_reservations",
        verbose_name="cancelled by",
    )
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="cancelled at")

    attendance_status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_CHOICES,
        default=ATTENDANCE_PENDING,
        verbose_name="attendance status",
    )
    attendance_marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendance_reservations",
        verbose_name="attendance marked by",
    )
    attendance_marked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="attendance marked at",
    )

    manager_decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES,
        default=DECISION_PENDING,
        verbose_name="manager decision",
    )
    manager_decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_reservation_decisions",
        verbose_name="manager decided by",
    )
    manager_decided_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="manager decided at",
    )

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="create date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="update date")

    class Meta:
        verbose_name = "3. Reservation"
        verbose_name_plural = "3. Reservations"
        ordering = ["-start_time"]

    @property
    def table_total(self):
        return self.table_unit_price * self.people_count

    @property
    def food_total(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def total_cost(self):
        return self.table_total + self.food_total

    def can_user_cancel(self, now=None):
        now = now or timezone.now()
        return self.status == self.STATUS_RESERVED and now < self.start_time

    def can_manager_cancel(self, now=None):
        now = now or timezone.now()
        return self.status == self.STATUS_RESERVED and now < (self.start_time - timedelta(hours=1))

    def can_mark_attendance(self, now=None):
        now = now or timezone.now()
        return self.status == self.STATUS_RESERVED and now >= self.start_time

    def can_leave_review(self, now=None):
        now = now or timezone.now()
        return (
            self.status == self.STATUS_RESERVED
            and now >= self.start_time
            and self.attendance_status == self.ATTENDANCE_PRESENT
        )

    def can_manager_decide(self):
        return self.status == self.STATUS_RESERVED

    def __str__(self):
        return f"Reservation #{self.id} - {self.user} - Table {self.table.table_number}"


class ReservationItem(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="reservation",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reservation_items",
        verbose_name="product",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="quantity")
    unit_price = models.PositiveIntegerField(verbose_name="unit price")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="create date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="update date")

    class Meta:
        verbose_name = "4. Reservation Item"
        verbose_name_plural = "4. Reservation Items"
        unique_together = ("reservation", "product")

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"



class Pay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    order = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='payment',
        null = True,
        blank = True
    )

    status = models.BooleanField(
        verbose_name='Paid',
        default=False
    )

    create_date = models.DateTimeField(
        verbose_name='create date',
        auto_now_add=True
    )

    update_date = models.DateTimeField(
        verbose_name='update date',
        auto_now=True
    )

    class Meta:
        verbose_name = "2. Pay"

    def __str__(self):
        return str(self.user)
