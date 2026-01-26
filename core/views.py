from django.shortcuts import render, get_object_or_404 
from .models import Cliente

# Create your views here.
from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

def calendario(request):
    return render(request, 'calendario.html')

def landing_personalizada(request, slug_cliente):
    cliente = get_object_or_404(Cliente, slug=slug_cliente)
    return render(request, 'landing.html', {'cliente': cliente})