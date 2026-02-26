from django.contrib import admin
from .models import Pay, Reservation, ReservationItem
# Register your models here.


admin.site.register(Reservation)
admin.site.register(ReservationItem)
admin.site.register(Pay)

