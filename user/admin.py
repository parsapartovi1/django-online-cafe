from django.contrib import admin

from serveHub.models import Category

from .models import User, Comment,Reply , WorkingShift
# Register your models here.


admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(WorkingShift)
