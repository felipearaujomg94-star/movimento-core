from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Conselho', {'fields': ('cargo',)}),
    )
    list_display = ['username', 'email', 'cargo', 'is_staff']


admin.site.register(Usuario, UsuarioAdmin)