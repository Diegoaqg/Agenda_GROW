# google_calendar.py
import os
from datetime import timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def crear_evento_google(reserva):
    # Ruta al JSON que ya probamos
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    ID_CALENDARIO = 'tigidmusic@gmail.com'
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        evento = {
            'summary': f'Sesión: {reserva.nombre_empresa}',
            'location': 'Videollamada / Oficina',
            'description': f'Contacto: {reserva.nombre_contacto}\nNotas: {reserva.notas}',
            'start': {
                'dateTime': reserva.fecha_inicio.isoformat(),
                'timeZone': 'America/Bogota', # Ajusta a tu zona
            },
            'end': {
                'dateTime': reserva.fecha_fin.isoformat(),
                'timeZone': 'America/Bogota',
            }
        }

        # 'primary' funciona porque le diste permisos al robot en el calendario principal
        resultado = service.events().insert(calendarId=ID_CALENDARIO, body=evento).execute()
        return resultado.get('id')
    except Exception as e:
        print(f"Error sincronizando con Google: {e}")
        return None
    
# google_calendar.py

def obtener_eventos_google(fecha_min, fecha_max):
    # Configuramos la ruta al JSON y credenciales (igual que crear_evento)
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # Permiso de lectura
    ID_CALENDARIO = 'tu-email-real@gmail.com' # <--- Asegúrate que sea el mismo de antes

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        # Pedimos la lista de eventos en el rango de tiempo
        events_result = service.events().list(
            calendarId=ID_CALENDARIO,
            timeMin=fecha_min,
            timeMax=fecha_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        print(f"Error leyendo Google Calendar: {e}")
        return []