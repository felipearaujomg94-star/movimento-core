from django.core.management.base import BaseCommand
from icalendar import Calendar
from institucional.models import Evento
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Importa eventos de um arquivo .ics para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('caminho_arquivo', type=str)

    def handle(self, *args, **options):
        caminho = options['caminho_arquivo']
        tz_brasil = pytz.timezone('America/Sao_Paulo')

        with open(caminho, 'rb') as f:
            cal = Calendar.from_ical(f.read())

        criados = 0
        ignorados = 0

        for componente in cal.walk():
            if componente.name != 'VEVENT':
                continue

            dtstart = componente.get('dtstart').dt

            if isinstance(dtstart, datetime):
                dtstart_local = dtstart.astimezone(tz_brasil)
                data = dtstart_local.date()
                horario = dtstart_local.time()
            else:
                data = dtstart
                horario = None

            atividade = str(componente.get('summary', 'Sem título'))
            local = str(componente.get('location', ''))
            observacao = str(componente.get('description', ''))

            existe = Evento.objects.filter(
                data=data, atividade=atividade
            ).exists()

            if existe:
                ignorados += 1
                continue

            Evento.objects.create(
                data=data,
                horario=horario,
                atividade=atividade,
                local=local,
                observacao=observacao,
            )
            criados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{criados} eventos importados, {ignorados} já existiam e foram ignorados.'
            )
        )