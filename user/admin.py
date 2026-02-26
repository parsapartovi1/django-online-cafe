from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Comment, Reply, User
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ("number",)
    list_display = ("number", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("number", "email", "first_name", "last_name")
    readonly_fields = ("create_date", "last_update", "last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("number", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "user_rate", "user_presence")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "create_date", "last_update")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("number", "email", "first_name", "last_name", "password1", "password2", "is_staff", "is_superuser", "is_active"),
            },
        ),
    )


admin.site.register(Comment)
admin.site.register(Reply)

