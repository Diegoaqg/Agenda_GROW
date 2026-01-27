import json
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Reserva
# Importamos la función que creamos en google_calendar.py
from .google_calendar import crear_evento_google
# Create your views here.
from django.shortcuts import render
from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from .google_calendar import obtener_eventos_google

def landing(request):
    return render(request, 'landing.html')

def landing_personalizada(request, slug_cliente):
    cliente = get_object_or_404(Cliente, slug=slug_cliente)
    return render(request, 'landing.html', {'cliente': cliente})

def mostrar_calendario(request, slug_cliente):
    cliente = get_object_or_404(Cliente, slug=slug_cliente)
    
    # Capturamos los datos que vienen de la landing (por la URL)
    servicio = request.GET.get('servicio')
    tipo = request.GET.get('tipo')
    detalles = request.GET.get('detalles')

    context = {
        'cliente': cliente,
        'servicio': servicio,
        'tipo': tipo,
        'detalles': detalles,
    }
    return render(request, 'calendario.html', context)

def confirmar_reserva(request, slug_cliente):
    cliente = get_object_or_404(Cliente, slug=slug_cliente)
    
    if request.method == 'POST':
        try:
            # Capturamos los datos
            fecha_str = request.POST.get('fecha_hora')
            email = request.POST.get('email')
            nombre = request.POST.get('nombre_contacto')
            
            # LOG DE SEGURIDAD: Esto saldrá en tu terminal de VS Code
            print(f"DEBUG: Intentando reservar para {nombre} en {fecha_str}")

            fecha_inicio = parse_datetime(fecha_str)
            
            # 1. Crear Reserva
            reserva = Reserva.objects.create(
                nombre_empresa=cliente.nombre,
                nombre_contacto=nombre,
                email=email,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_inicio + timedelta(hours=1),
                notas=f"Servicio: {request.POST.get('servicio')}"
            )
            
            print(f"DEBUG: Reserva guardada en DB con ID: {reserva.id}")

            # 2. Google
            google_id = crear_evento_google(reserva)
            if google_id:
                reserva.google_event_id = google_id
                reserva.sincronizado_google = True
                reserva.save()
                print("DEBUG: Sincronizado con Google con éxito")

            return render(request, 'exito.html', {'reserva': reserva, 'cliente': cliente})

        except Exception as e:
            # Si algo falla, lo veremos en la terminal
            print(f"ERROR CRÍTICO: {e}")
            return render(request, 'calendario.html', {'cliente': cliente, 'error': str(e)})
            
    return redirect('landing_pro', slug_cliente=slug_cliente)

def api_eventos_google(request, slug_cliente):
    # FullCalendar envía automáticamente el rango de fechas que está mostrando
    start_iso = request.GET.get('start')
    end_iso = request.GET.get('end')
    
    # Llamamos a nuestra nueva función de Google
    google_events = obtener_eventos_google(start_iso, end_iso)
    
    eventos_formateados = []
    for event in google_events:
        # Extraemos la fecha de inicio y fin del evento de Google
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        eventos_formateados.append({
            'title': 'Ocupado', # Por privacidad, no mostramos el nombre del evento real
            'start': start,
            'end': end,
            'color': '#ff4b4b', # Rojo para indicar que no está disponible
            'display': 'block', # Bloque sólido
        })
        
    return JsonResponse(eventos_formateados, safe=False)