import os.path
import datetime as dt
import random
import sqlite3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

lista_frases=[
    "'Nuestra tarea debe ser liberarnos de esta prisión ampliando nuestro círculo de compasión para abrazar a todas las criaturas vivientes y a toda la naturaleza en su belleza.' -A. Einstein", 
    "'Sentí que mis pulmones se inflaban con la avalancha del paisaje: aire, montañas, árboles, gente. Pensé: Esto es lo que es ser feliz.' -S. Plath",
    "'...y luego tengo la naturaleza y el arte y la poesía, y si eso no es suficiente, ¿cuánto es suficiente?' -V. Van Gogh",
    "'Las montañas están llamando y debo ir.' -J. Muir",
    "'Adopta el ritmo de la naturaleza: su secreto es la paciencia.' -R. W. Emerson",
    "'Vive cada estación como pase; respira el aire, bebe el agua, prueba la fruta, y resígnate a la influencia de la Tierra' -H. D. Thoreau",
    "'Las estrellas son como árboles en el bosque, vivas y respirando. Y me están observando.' -H. Murakami",
    "'El objetivo de la vida es hacer que el ritmo de tu corazón se alinee con el ritmo del universo, alinear tu naturaleza con la naturaleza.' -J. Campbell"
]
dias="TH"
opcion=0
apodos=["Corazón5", "Amiguín4", "Bombón3", "Cosita2"] #🍑🍎🍆🥦
d_actual=dt.datetime.now()
fecha=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}"

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

def modificar(id, nuevos_dias): #actualizar evento existente
    # Datos a actualizar
    update_data = {
        'recurrence': [f"RRULE:FREQ=WEEKLY;BYDAY={nuevos_dias};COUNT=12"]
    }

    # Actualizar el evento
    updated_event = service.events().patch(calendarId='primary', eventId=id, body=update_data).execute()

    print('Evento actualizado:', updated_event.get('recurrence'))

try:
    service = build("calendar", "v3", credentials=creds)

    event_id = "tngtnbhqqfuu1tvc25u6n3802s"
    new_dias="WE"

    modificar(event_id, new_dias)

    # event = {
    #     "summary": f"¡A reciclar {apodos[opcion][:-1]}!",
    #     "location": "Santiago",
    #     "description": f"¡A despertar {apodos[opcion][:-1]}! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. {lista_frases[random.randint(0, len(lista_frases)-1)]}",
    #     "colorId": int(apodos[opcion][-1]),
    #     "start": {
    #         "date":  fecha, #"aaaa-mm-dd"
    #         "timeZone": "America/Santiago"
    #     },
    #     "end": {
    #         "date":  fecha,
    #         "timeZone": "America/Santiago"
    #     },
    #     "recurrence": [
    #         f"RRULE:FREQ=WEEKLY;BYDAY={dias};COUNT=12"
    #     ]
    # }

    # event = service.events().insert(calendarId='primary', body=event).execute()
    # # Almacenar la ID del evento creado
    # evento_id = event['id']

    # print(f"Evento creado exitosamente: {event.get('htmlLink')}")
    # print(f"ID evento: {evento_id}")

except HttpError as error:
    print("Ha ocurrido un error: ", error)