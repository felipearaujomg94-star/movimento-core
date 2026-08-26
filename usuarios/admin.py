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
                    "is_staff",
                    "is_active",
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

    def usuario_e_superusuario(self, request):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.is_superuser
        )

    def has_module_permission(self, request):
        return self.usuario_e_superusuario(request)

    def has_view_permission(self, request, obj=None):
        return self.usuario_e_superusuario(request)

    def has_add_permission(self, request):
        return self.usuario_e_superusuario(request)

    def has_change_permission(self, request, obj=None):
        return self.usuario_e_superusuario(request)

    def has_delete_permission(self, request, obj=None):
        return self.usuario_e_superusuario(request)