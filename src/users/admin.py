from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ["email", "first_name", "last_name", "last_login", "is_active", "is_staff", "is_superuser"]
    list_display_links = ["email", "first_name", "last_name"]
    list_editable = ["is_active", "is_staff"]
    readonly_fields = ["password", "last_login", "created", "last_update"]
    ordering = ["-created", "-pk"]
    filter_horizontal = []
    list_filter = []
    fieldsets = [
        [None, {"fields": ["email", "password"]}],
        ["Personal Info", {"fields": ["first_name", "last_name"]}],
        ["Permissions", {"fields": ["is_active", "is_staff", "is_superuser"]}],
        ["Important Dates", {"fields": ["created", "last_update", "last_login"]}],
    ]
    add_fieldsets = [
        [None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2")
        }],
    ]


admin.site.register(User, CustomUserAdmin)
