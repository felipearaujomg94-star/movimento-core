from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Evento, EventoRealizado


class EventoAdminForm(forms.ModelForm):
    confirmar_alteracao_data = forms.BooleanField(
        required=False,
        label="Confirmo que desejo alterar a data deste evento",
        help_text=(
            "Marque esta opção somente quando estiver alterando "
            "a data de um evento já existente."
        ),
    )

    class Meta:
        model = Evento
        fields = "__all__"

        widgets = {
            "data": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
            "horario": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # A confirmação não aparece na criação de um evento.
        if not self.instance or not self.instance.pk:
            self.fields.pop(
                "confirmar_alteracao_data",
                None,
            )

    def clean(self):
        cleaned_data = super().clean()

        if self.instance and self.instance.pk:
            data_nova = cleaned_data.get("data")

            data_original = (
                Evento.objects
                .filter(pk=self.instance.pk)
                .values_list("data", flat=True)
                .first()
            )

            alterou_data = (
                data_nova
                and data_original
                and data_nova != data_original
            )

            confirmou = cleaned_data.get(
                "confirmar_alteracao_data"
            )

            if alterou_data and not confirmou:
                raise ValidationError(
                    "A data deste evento foi alterada. "
                    "Marque a confirmação antes de salvar."
                )

        return cleaned_data


class BaseEventoAdmin(admin.ModelAdmin):
    form = EventoAdminForm

    list_display = [
        "data",
        "horario",
        "atividade",
        "local",
    ]

    list_filter = [
        "data",
    ]

    date_hierarchy = "data"

    search_fields = [
        "atividade",
        "local",
        "observacao",
    ]


@admin.register(Evento)
class EventoAdmin(BaseEventoAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.filter(
            data__gte=timezone.localdate()
        )


@admin.register(EventoRealizado)
class EventoRealizadoAdmin(BaseEventoAdmin):
    ordering = [
        "-data",
        "-horario",
    ]

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.filter(
            data__lt=timezone.localdate()
        )