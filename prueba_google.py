import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# 1. Configuración de credenciales
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 2. PON AQUÍ TU CORREO (el mismo al que le compartiste acceso)
CALENDAR_ID = 'tigidmusic@gmail.com' 

def test_conexion():
    try:
        print("🚀 Iniciando conexión con Google...")
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        # Crear un evento para hoy mismo en 30 minutos
        inicio = datetime.utcnow() + timedelta(minutes=30)
        fin = inicio + timedelta(hours=1)

        evento = {
            'summary': '✅ ¡CONEXIÓN EXITOSA!',
            'description': 'Si ves esto, Django ya puede hablar con tu Google Calendar.',
            'start': {'dateTime': inicio.isoformat() + 'Z'},
            'end': {'dateTime': fin.isoformat() + 'Z'},
        }

        print("📡 Enviando evento a Google...")
        resultado = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
        
        print("-" * 30)
        print(f"🔥 ¡LOGRADO! Evento creado con éxito.")
        print(f"🔗 Puedes verlo aquí: {resultado.get('htmlLink')}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ Error detectado: {e}")

if __name__ == '__main__':
    test_conexion()