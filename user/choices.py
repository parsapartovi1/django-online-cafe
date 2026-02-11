from django.db import models


class WeekDays(models.TextChoices):
    SATURDAY = 'S', 'Saturday'
    SUNDAY = 'SU', 'Sunday'
    MONDAY = 'M', 'Monday'
    TUESDAY = 'T', 'Tuesday'
    WEDNESDAY = 'W', 'Wednesday'
    THURSDAY = 'Th', 'Thursday'
    FRIDAY = 'F', 'Friday'