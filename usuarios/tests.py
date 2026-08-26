from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.test import SimpleTestCase

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
            cargos["secretaria"],
            "Secretaria",
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
            "Maria Silva (Secretaria)",
        )


class UsuarioAdminTests(SimpleTestCase):
    def setUp(self):
        self.usuario_admin = UsuarioAdmin(
            Usuario,
            admin.site,
        )

    def test_formulario_de_criacao_exibe_email_e_cargo(self):
        campos = flatten_fieldsets(
            self.usuario_admin.add_fieldsets
        )

        self.assertIn("email", campos)
        self.assertIn("cargo", campos)

    def test_lista_exibe_e_filtra_por_cargo(self):
        self.assertIn(
            "cargo",
            self.usuario_admin.list_display,
        )
        self.assertIn(
            "cargo",
            self.usuario_admin.list_filter,
        )