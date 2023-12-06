import os.path
from datetime import datetime, timedelta
# import random
# import sqlite3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# SCOPES = ["https://www.googleapis.com/auth/calendar"]

# lista_frases=[
#     "'Nuestra tarea debe ser liberarnos de esta prisión ampliando nuestro círculo de compasión para abrazar a todas las criaturas vivientes y a toda la naturaleza en su belleza.' -A. Einstein", 
#     "'Sentí que mis pulmones se inflaban con la avalancha del paisaje: aire, montañas, árboles, gente. Pensé: Esto es lo que es ser feliz.' -S. Plath",
#     "'...y luego tengo la naturaleza y el arte y la poesía, y si eso no es suficiente, ¿cuánto es suficiente?' -V. Van Gogh",
#     "'Las montañas están llamando y debo ir.' -J. Muir",
#     "'Adopta el ritmo de la naturaleza: su secreto es la paciencia.' -R. W. Emerson",
#     "'Vive cada estación como pase; respira el aire, bebe el agua, prueba la fruta, y resígnate a la influencia de la Tierra' -H. D. Thoreau",
#     "'Las estrellas son como árboles en el bosque, vivas y respirando. Y me están observando.' -H. Murakami",
#     "'El objetivo de la vida es hacer que el ritmo de tu corazón se alinee con el ritmo del universo, alinear tu naturaleza con la naturaleza.' -J. Campbell"
# ]
# dias="SA"
# opcion=2
# apodos=["Corazón5", "Amiguín4", "Bombón3", "Cosita2"] #🍑🍎🍆🥦
# d_actual=dt.datetime.now()
# fecha=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}"

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

# def modificar(id, nuevos_dias): #actualizar evento
#     # Datos a actualizar
#     update_data = {
#         'recurrence': [f"RRULE:FREQ=WEEKLY;BYDAY={nuevos_dias};COUNT=12"]
#     }

#     # Actualizar el evento
#     updated_event = service.events().patch(calendarId='primary', eventId=id, body=update_data).execute()
#     print('Evento actualizado:', updated_event.get('recurrence'))

# def eliminar(id): #eliminar evento
#     service.events().delete(calendarId='primary', eventId=id).execute()
#     print('Evento eliminado:', id)

# try:
#     service = build("calendar", "v3", credentials=creds)

#     event_id = ""
#     new_dias="WE"

#     # modificar(event_id, new_dias)
#     # eliminar(event_id)

#     # #crear evento
#     # event = {
#     #     "summary": f"¡A reciclar {apodos[opcion][:-1]}!",
#     #     "location": "Santiago",
#     #     "description": f"¡A despertar {apodos[opcion][:-1]}! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. {lista_frases[random.randint(0, len(lista_frases)-1)]}",
#     #     "colorId": int(apodos[opcion][-1]),
#     #     "start": {
#     #         "date":  fecha, #"aaaa-mm-dd"
#     #         "timeZone": "America/Santiago"
#     #     },
#     #     "end": {
#     #         "date":  fecha,
#     #         "timeZone": "America/Santiago"
#     #     },
#     #     "recurrence": [
#     #         f"RRULE:FREQ=WEEKLY;BYDAY={dias};COUNT=12"
#     #     ]
#     # }

#     # event = service.events().insert(calendarId='primary', body=event).execute()
#     # # Almacenar la ID del evento creado
#     # evento_id = event['id']

#     # print(f"Evento creado exitosamente: {event.get('htmlLink')}")
#     # print(f"ID evento: {evento_id}")

#     # #---cierre crear evento

# except HttpError as error:
#     print("Ha ocurrido un error: ", error)


# evento_id="BYUVbuvytUBpatatillasconludillas"
# correo="correo9"

# con = sqlite3.connect("db.sqlite3")
# cur = con.cursor()

# cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
# ant=cur.fetchone()[0]
# cur.execute(f"UPDATE Recycle_usuario SET id_evento='{evento_id}' WHERE correo='{correo}'")
# cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
# nue=cur.fetchone()[0]

# print(f"ID guardada: de '{ant}' -> '{nue}'")
# con.commit()
# con.close()

service = build("calendar", "v3", credentials=creds)

event_id = "br3i94kdcsgj1k819u6cmshctg"
# event = service.events().get(calendarId='primary', eventId=event_id).execute()

d_actual=datetime.now()
fecha_actual=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}" #"2023-12-03"

# Define el día específico que quieres consultar (en este caso, 1 de enero de 2024)
day_to_check = datetime(int(d_actual.strftime('%Y')), int(d_actual.strftime('%m')), int(d_actual.strftime('%d')))

# Define el intervalo de tiempo para la consulta (desde la medianoche hasta la medianoche del día siguiente)
start_time = day_to_check.isoformat() + 'Z'
end_time = (day_to_check + timedelta(days=1)).isoformat() + 'Z'

print(day_to_check)
print(start_time)
print(end_time)

# Realiza la consulta a la API para obtener los eventos del día especificado
events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=end_time, singleEvents=True).execute()
events = events_result.get('items', [])
# print("")
# print(events)

def eliminar(id): #eliminar evento 
    service.events().delete(calendarId='primary', eventId=id).execute()
    print('Evento eliminado:', id)

# Imprime los eventos del día
if not events:
    print('No hay eventos para este día.')
else:
    print('Eventos del día:')
    for event in events:
        print(f"- {event['summary']} - {event['start'].get('dateTime', event['start'].get('date'))} - {event['id'][:-9]}")

        if event['id'][:-9]==event_id:
            print(event)
            # #eliminar evento
            # eliminar(event_id)
