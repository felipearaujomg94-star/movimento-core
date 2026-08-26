from datetime import timedelta

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .admin import (
    EventoAdmin,
    EventoAdminForm,
    EventoRealizadoAdmin,
)
from .models import Evento, EventoRealizado


class EventoAdminQuerysetTests(TestCase):
    def setUp(self):
        self.hoje = timezone.localdate()
        self.request = RequestFactory().get("/admin/")

        self.evento_passado = Evento.objects.create(
            data=self.hoje - timedelta(days=1),
            atividade="Evento passado",
        )

        self.evento_hoje = Evento.objects.create(
            data=self.hoje,
            atividade="Evento de hoje",
        )

        self.evento_futuro = Evento.objects.create(
            data=self.hoje + timedelta(days=1),
            atividade="Evento futuro",
        )

    def test_eventos_mostra_hoje_e_futuros(self):
        evento_admin = EventoAdmin(
            Evento,
            admin.site,
        )

        queryset = evento_admin.get_queryset(self.request)

        self.assertSetEqual(
            set(queryset.values_list("pk", flat=True)),
            {
                self.evento_hoje.pk,
                self.evento_futuro.pk,
            },
        )

    def test_eventos_realizados_mostra_somente_passados(self):
        evento_realizado_admin = EventoRealizadoAdmin(
            EventoRealizado,
            admin.site,
        )

        queryset = evento_realizado_admin.get_queryset(
            self.request
        )

        self.assertSetEqual(
            set(queryset.values_list("pk", flat=True)),
            {
                self.evento_passado.pk,
            },
        )

    def test_eventos_realizados_nao_permite_adicionar(self):
        evento_realizado_admin = EventoRealizadoAdmin(
            EventoRealizado,
            admin.site,
        )

        permite_adicionar = (
            evento_realizado_admin.has_add_permission(
                self.request
            )
        )

        self.assertFalse(permite_adicionar)


class EventoAdminFormTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            data=timezone.localdate(),
            horario="08:00",
            atividade="Evento de teste",
            local="Local de teste",
            observacao="Observação de teste",
        )

    def dados_do_formulario(self):
        return {
            "data": self.evento.data.isoformat(),
            "horario": "08:00",
            "atividade": self.evento.atividade,
            "local": self.evento.local,
            "observacao": self.evento.observacao,
        }

    def test_alteracao_de_data_exige_confirmacao(self):
        dados = self.dados_do_formulario()
        dados["data"] = (
            self.evento.data + timedelta(days=1)
        ).isoformat()

        formulario = EventoAdminForm(
            data=dados,
            instance=self.evento,
        )

        self.assertFalse(formulario.is_valid())
        self.assertIn(
            "A data deste evento foi alterada.",
            str(formulario.non_field_errors()),
        )

    def test_alteracao_de_data_com_confirmacao_e_valida(self):
        dados = self.dados_do_formulario()
        dados["data"] = (
            self.evento.data + timedelta(days=1)
        ).isoformat()
        dados["confirmar_alteracao_data"] = "on"

        formulario = EventoAdminForm(
            data=dados,
            instance=self.evento,
        )

        self.assertTrue(formulario.is_valid())

    def test_alteracao_somente_de_horario_e_valida(self):
        dados = self.dados_do_formulario()
        dados["horario"] = "09:30"

        formulario = EventoAdminForm(
            data=dados,
            instance=self.evento,
        )

        self.assertTrue(formulario.is_valid())