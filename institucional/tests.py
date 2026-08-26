from datetime import timedelta

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from usuarios.models import Usuario

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

        queryset = evento_admin.get_queryset(
            self.request
        )

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


class EventoAdminPermissionTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        self.evento_admin = EventoAdmin(
            Evento,
            admin.site,
        )

        self.evento_realizado_admin = (
            EventoRealizadoAdmin(
                EventoRealizado,
                admin.site,
            )
        )

    def criar_request(
        self,
        cargo="",
        superusuario=False,
        staff=True,
        ativo=True,
    ):
        request = self.request_factory.get("/admin/")

        request.user = Usuario(
            username="usuario-teste",
            cargo=cargo,
            is_superuser=superusuario,
            is_staff=staff,
            is_active=ativo,
        )

        return request

    def verificar_permissoes_de_gestao(
        self,
        model_admin,
        request,
        permite_adicionar=True,
    ):
        self.assertTrue(
            model_admin.has_module_permission(request)
        )
        self.assertTrue(
            model_admin.has_view_permission(request)
        )
        self.assertEqual(
            model_admin.has_add_permission(request),
            permite_adicionar,
        )
        self.assertTrue(
            model_admin.has_change_permission(request)
        )
        self.assertTrue(
            model_admin.has_delete_permission(request)
        )

    def verificar_permissoes_de_consulta(
        self,
        model_admin,
        request,
    ):
        self.assertTrue(
            model_admin.has_module_permission(request)
        )
        self.assertTrue(
            model_admin.has_view_permission(request)
        )
        self.assertFalse(
            model_admin.has_add_permission(request)
        )
        self.assertFalse(
            model_admin.has_change_permission(request)
        )
        self.assertFalse(
            model_admin.has_delete_permission(request)
        )

    def test_cargos_autorizados_podem_gerenciar_eventos(self):
        cargos_autorizados = (
            Usuario.Cargo.COORDENACAO,
            Usuario.Cargo.PADRE,
            Usuario.Cargo.SECRETARIA,
        )

        for cargo in cargos_autorizados:
            with self.subTest(cargo=cargo):
                request = self.criar_request(
                    cargo=cargo
                )

                self.verificar_permissoes_de_gestao(
                    self.evento_admin,
                    request,
                )

                self.verificar_permissoes_de_gestao(
                    self.evento_realizado_admin,
                    request,
                    permite_adicionar=False,
                )

    def test_demais_cargos_podem_apenas_consultar(self):
        cargos_de_consulta = (
            Usuario.Cargo.LITURGIA,
            Usuario.Cargo.TESOURARIA,
            Usuario.Cargo.MARKETING,
        )

        for cargo in cargos_de_consulta:
            with self.subTest(cargo=cargo):
                request = self.criar_request(
                    cargo=cargo
                )

                self.verificar_permissoes_de_consulta(
                    self.evento_admin,
                    request,
                )

                self.verificar_permissoes_de_consulta(
                    self.evento_realizado_admin,
                    request,
                )

    def test_usuario_sem_acesso_ao_admin_nao_ve_eventos(self):
        request = self.criar_request(
            cargo=Usuario.Cargo.COORDENACAO,
            staff=False,
        )

        self.assertFalse(
            self.evento_admin.has_module_permission(
                request
            )
        )
        self.assertFalse(
            self.evento_admin.has_view_permission(
                request
            )
        )

    def test_superusuario_pode_gerenciar_eventos(self):
        request = self.criar_request(
            superusuario=True,
        )

        self.verificar_permissoes_de_gestao(
            self.evento_admin,
            request,
        )

        self.verificar_permissoes_de_gestao(
            self.evento_realizado_admin,
            request,
            permite_adicionar=False,
        )