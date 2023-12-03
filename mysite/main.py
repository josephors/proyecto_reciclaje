import os.path
import datetime as dt
import random
import sqlite3

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"] #"Each API defines one or more scopes that declare a set of operations permitted". Esta API de calendario define un set de operaciones para CALENDAR.

def modificar(id, nuevos_dias): #actualizar evento existente
    # Datos a actualizar
    update_data = {
        'recurrence': [f"RRULE:FREQ=WEEKLY;BYDAY={nuevos_dias};COUNT=12"]
    }

    # Actualizar el evento
    updated_event = service.events().patch(calendarId='primary', eventId=id, body=update_data).execute()

    print('Evento actualizado:', updated_event.get('recurrence'))

def main():
    #creación token / acceso a cuenta google
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
            token.write(creds.to_json()) #usamos el token recién creado(?)

    # #variables formulario
    # nombre="Matias" #***FORMULARIO_NOMBRE***
    # correo="hola@gmail.com" #***FORMULARIO_CORREO***
    # datos_usuario=[nombre, correo]

    #frases aleatorias
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

    #variables formulario 2
    dias="SU"
    opcion=3
    datos_calendario=[dias, opcion]

    apodos=["Corazón5", "Amiguín4", "Bombón3", "Cosita2"] #🍑🍎🍆🥦
    d_actual=dt.datetime.now()
    fecha=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}" #2023-11-30

    #creación evento
    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": f"¡A reciclar {apodos[opcion][:-1]}!",
            "location": "Santiago",
            "description": f"¡A despertar {apodos[opcion][:-1]}! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. {lista_frases[random.randint(0, len(lista_frases)-1)]}",
            "colorId": int(apodos[opcion][-1]),
            "start": {
                "date":  fecha, #"aaaa-mm-dd" #hay un error y es que está marcando este día como primero. Debe ser el primer domingo o el primer día siguiente
                "timeZone": "America/Santiago"
            },
            "end": {
                "date":  fecha,
                "timeZone": "America/Santiago"
            },
            "recurrence": [
                f"RRULE:FREQ=WEEKLY;BYDAY={dias};COUNT=12"
            ]
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Evento creado exitosamente: {event.get('htmlLink')}")

        #guardar en base de datos la id del evento
        evento_id = event['id']
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute(f"UPDATE Recycle_usuario SET id_evento={evento_id} WHERE correo='{correo}'")
        print(f"Evento guardado exitosamente: {event.get('htmlLink')}")
        con.commit()
        con.close()

        # #modificar evento existente
        # event_id = "tngtnbhqqfuu1tvc25u6n3802s"
        # new_dias="SA"
        # modificar(event_id, new_dias)

        #eliminar evento existente
        #***

    except HttpError as error:
        print("Ha ocurrido un error: ", error)


if __name__ == "__main__":
    main()