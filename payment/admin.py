from django.contrib import admin
from .models import Order, Pay, Reservation, ReservationItem
# Register your models here.


admin.site.register(Order)
admin.site.register(Pay)
admin.site.register(Reservation)
admin.site.register(ReservationItem)
