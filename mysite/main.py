import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None

    if os.path.exists("token.json"): #si es que ya tenemos un token creado para usar como credencial...
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid: #si es que no existen credenciales o no son válidas...
        if creds and creds.expired and creds.refresh_token: #si es que las credenciales existen pero están expiradas y necesitan ser actualidazas...
            creds.refresh(Request())
        else: #si es que las credenciales no existen directamente..
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json()) #usamos el token recién creado(?)

    #habiendo accedido a los datos, al usuario y a su cuenta, ejecutaremos la aplicación/acción per se:
    try:
        service = build("calendar", "v3", credentials=creds)

        event = { #creamos un diccionario que representa el evento. Es el evento per se, y cada llave representa una característica de este (consultar documentación).
            "summary": "Fiesta de la puta madre",
            "location": "Rosario Central",
            "description": "***",
            "colorId": 3,
            "start": {
                "dateTime": "2023-11-11T17:00:00-04:00",
                "timeZone": "Europe/Vienna" #***
            },
            "end": {
                "dateTime": "2023-11-11T23:00:00-04:00",
                "timeZone": "Europe/Vienna" #***
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=2"
            ],
            "attendees": [
                {"email": "salvadorwwwww2@gmail.com"},
                {"email": "gonzalocwwww@gmail.com"},
                {"email": "javierganswwww@gmail.com"}
            ],
            "locked": True
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Evento creado exitosamente: {event.get('htmlLink')}")

        # para retornar eventos del calendario del usuario
        # now = dt.datetime.now().isoformat()+"Z"

        # event_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute() #nos listará/retornará los 10 próximos eventos de nuestro calendario.

        # events = event_result.get("items", []) #creo que saca, del objeto retornado, aquellos calificados como "items" (o que se encuentren en una sección del mismo nombre) y los guarda en una lista.

        # if not events: #si no se retornó ningún evento...
        #     print("No se encontraron eventos próximamente")
        #     return
        
        # for event in events: #para cada "i" en la lista events...
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"]) #...guardaremos en una variable el valor de la llave "start" retornado por get, que es la fecha de comienzo, y lo mostraremos en la consola junto con el valor de la llave "summary", que supongo que es el nombre y/o descripción del evento.

    except HttpError as error: #si durante la ejecución del try se produce un error del tipo Http, se atrapará, asignará a la variable "error" y se ejecutará el siguiente código...
        print("Ha ocurrido un error: ", error)

if __name__ == "__main__": #***
    main()