import os.path
import datetime as dt
import sqlite3

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"] #"Each API defines one or more scopes that declare a set of operations permitted". Esta API de calendario define un set de operaciones para CALENDAR.

def main():
    nombre="***FORMULARIO_NOMBRE***"
    correo="***FORMULARIO_CORREO"
    opcion="***FORMULARIO_OPCION***"
    dias="***FORMULARIO_DIASELEGIDOS (MON, TUE)***"
    datos_usuario=[nombre, correo]
    datos_calendario=[dias, opcion]
    lista_frases=[
        "Nuestra tarea debe ser liberarnos de esta prisión ampliando nuestro círculo de compasión para abrazar a todas las criaturas vivientes y a toda la naturaleza en su belleza. -A. Einstein", 
        "Sentí que mis pulmones se inflaban con la avalancha del paisaje: aire, montañas, árboles, gente. Pensé: Esto es lo que es ser feliz. -Sylvia Plath",
        "...y luego tengo la naturaleza y el arte y la poesía, y si eso no es suficiente, ¿cuánto es suficiente? -V. Van Gogh"
    ]

    #creación evento
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": "¡A reciclar Succionador!",
            "location": "Santiago",
            "description": "¡A despertar Bombón! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. 'Nuestra tarea debe ser liberarnos de esta prisión ampliando nuestro círculo de compasión para abrazar a todas las criaturas vivientes y a toda la naturaleza en su belleza' -A. Einstein",
            "colorId": 3,
            "start": {
                "date":  "2023-12-11", #"aaaa-mm-dd"
                "timeZone": "America/Santiago"
            },
            "end": {
                "date":  "2023-12-11",
                "timeZone": "America/Santiago"
            },
            "recurrence": [
                "RRULE:FREQ=WEEKLY;COUNT=2"
            ]
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Evento creado exitosamente: {event.get('htmlLink')}")

    except HttpError as error:
        print("Ha ocurrido un error: ", error)

if __name__ == "__main__":
    main()