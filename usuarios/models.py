from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    CARGO_CHOICES = [
        ('coordenacao', 'Coordenação'),
        ('secretaria', 'Secretaria'),
        ('liturgia', 'Liturgia'),
        ('tesouraria', 'Tesouraria'),
        ('marketing', 'Marketing'),
    ]

    cargo = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES,
        verbose_name='Cargo no conselho'
    )
    REQUIRED_FIELDS = ['cargo']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_cargo_display()})"