from django.db import models


class WeekDays(models.TextChoices):
    SATURDAY = 'S', 'Saturday'
    SUNDAY = 'S', 'Sunday'
    MONDAY = 'M', 'Monday'
    TUESDAY = 'T', 'Tuesday'
    WEDNESDAY = 'W', 'Wednesday'
    THURSDAY = 'T', 'Thursday'
    FRIDAY = 'F', 'Friday'