from django.db import models


class Evento(models.Model):
    data = models.DateField(verbose_name="Data")
    horario = models.TimeField(
        verbose_name="Horário",
        blank=True,
        null=True,
    )
    atividade = models.CharField(
        max_length=255,
        verbose_name="Atividade",
    )
    local = models.CharField(
        max_length=255,
        verbose_name="Local",
        blank=True,
    )
    observacao = models.CharField(
        max_length=255,
        verbose_name="Observação",
        blank=True,
    )

    class Meta:
        ordering = ["data", "horario"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return (
            f"{self.data.strftime('%d/%m/%Y')} - "
            f"{self.atividade}"
        )


class EventoRealizado(Evento):
    class Meta:
        proxy = True
        verbose_name = "Evento realizado"
        verbose_name_plural = "Eventos realizados"