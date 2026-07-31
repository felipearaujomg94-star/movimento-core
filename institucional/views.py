from django.shortcuts import render


def home(request):
    return render(request, 'institucional/home.html')

def sobre(request):
    return render(request, 'institucional/sobre.html')