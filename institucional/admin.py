from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['data', 'horario', 'atividade', 'local']
    list_filter = ['data']
    search_fields = ['atividade', 'local', 'observacao']