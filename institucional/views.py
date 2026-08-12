from django.shortcuts import render
from django.utils import timezone
from .models import Evento


def home(request):
    hoje = timezone.now().date()
    proximos_eventos = Evento.objects.filter(data__gte=hoje)[:3]

    return render(request, 'institucional/home.html', {
        'proximos_eventos': proximos_eventos
    })


def sobre(request):
    return render(request, 'institucional/sobre.html')


def eventos(request):
    hoje = timezone.now().date()
    proximos_eventos = Evento.objects.filter(data__gte=hoje)[:30]
    return render(request, 'institucional/eventos.html', {
        'eventos': proximos_eventos
    })