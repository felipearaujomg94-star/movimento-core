from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.test import RequestFactory, SimpleTestCase

from .admin import UsuarioAdmin
from .models import Usuario


class UsuarioModelTests(SimpleTestCase):
    def test_cargos_possuem_rotulos_corretos(self):
        cargos = dict(Usuario.Cargo.choices)

        self.assertEqual(
            cargos["coordenacao"],
            "Coordenação",
        )
        self.assertEqual(
            cargos["padre"],
            "Padre",
        )
        self.assertEqual(
            cargos["secretaria"],
            "Secretária",
        )
        self.assertEqual(
            cargos["liturgia"],
            "Liturgia",
        )
        self.assertEqual(
            cargos["tesouraria"],
            "Tesouraria",
        )
        self.assertEqual(
            cargos["marketing"],
            "Marketing",
        )

    def test_email_e_cargo_sao_campos_obrigatorios(self):
        self.assertIn(
            "email",
            Usuario.REQUIRED_FIELDS,
        )
        self.assertIn(
            "cargo",
            Usuario.REQUIRED_FIELDS,
        )

    def test_representacao_exibe_nome_e_cargo(self):
        usuario = Usuario(
            username="maria",
            first_name="Maria",
            last_name="Silva",
            cargo=Usuario.Cargo.SECRETARIA,
        )

        self.assertEqual(
            str(usuario),
            "Maria Silva (Secretária)",
        )


class UsuarioAdminTests(SimpleTestCase):
    def setUp(self):
        self.usuario_admin = UsuarioAdmin(
            Usuario,
            admin.site,
        )
        self.request_factory = RequestFactory()

    def criar_request(self, superusuario):
        request = self.request_factory.get("/admin/")
        request.user = Usuario(
            username="usuario-teste",
            cargo=Usuario.Cargo.COORDENACAO,
            is_active=True,
            is_staff=True,
            is_superuser=superusuario,
        )
        return request

    def test_formulario_de_criacao_exibe_campos_necessarios(self):
        campos = flatten_fieldsets(
            self.usuario_admin.add_fieldsets
        )

        self.assertIn("email", campos)
        self.assertIn("cargo", campos)
        self.assertIn("is_staff", campos)
        self.assertIn("is_active", campos)

    def test_lista_exibe_e_filtra_por_cargo(self):
        self.assertIn(
            "cargo",
            self.usuario_admin.list_display,
        )
        self.assertIn(
            "cargo",
            self.usuario_admin.list_filter,
        )

    def test_superusuario_pode_gerenciar_usuarios(self):
        request = self.criar_request(
            superusuario=True
        )

        self.assertTrue(
            self.usuario_admin.has_module_permission(
                request
            )
        )
        self.assertTrue(
            self.usuario_admin.has_view_permission(
                request
            )
        )
        self.assertTrue(
            self.usuario_admin.has_add_permission(
                request
            )
        )
        self.assertTrue(
            self.usuario_admin.has_change_permission(
                request
            )
        )
        self.assertTrue(
            self.usuario_admin.has_delete_permission(
                request
            )
        )

    def test_usuario_comum_nao_pode_gerenciar_usuarios(self):
        request = self.criar_request(
            superusuario=False
        )

        self.assertFalse(
            self.usuario_admin.has_module_permission(
                request
            )
        )
        self.assertFalse(
            self.usuario_admin.has_view_permission(
                request
            )
        )
        self.assertFalse(
            self.usuario_admin.has_add_permission(
                request
            )
        )
        self.assertFalse(
            self.usuario_admin.has_change_permission(
                request
            )
        )
        self.assertFalse(
            self.usuario_admin.has_delete_permission(
                request
            )
        )