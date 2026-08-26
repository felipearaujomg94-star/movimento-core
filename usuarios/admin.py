from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações do Conselho",
            {
                "fields": (
                    "cargo",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações do Conselho",
            {
                "fields": (
                    "email",
                    "cargo",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "cargo",
        "is_staff",
        "is_active",
    )

    list_filter = UserAdmin.list_filter + (
        "cargo",
    )