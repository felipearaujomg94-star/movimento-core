from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Cargo(models.TextChoices):
        COORDENACAO = "coordenacao", "Coordenação"
        SECRETARIA = "secretaria", "Secretaria"
        LITURGIA = "liturgia", "Liturgia"
        TESOURARIA = "tesouraria", "Tesouraria"
        MARKETING = "marketing", "Marketing"

    cargo = models.CharField(
        max_length=20,
        choices=Cargo.choices,
        verbose_name="Cargo no conselho",
    )

    REQUIRED_FIELDS = [
        *AbstractUser.REQUIRED_FIELDS,
        "cargo",
    ]

    def __str__(self):
        nome = self.get_full_name() or self.username

        if self.cargo:
            return f"{nome} ({self.get_cargo_display()})"

        return nome