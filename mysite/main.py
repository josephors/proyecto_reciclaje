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

def main():
    #declaración funciones
    def modificar(id, nuevos_dias): #actualizar evento 
        # Datos a actualizar
        update_data = {
            'recurrence': [f"RRULE:FREQ=WEEKLY;BYDAY={nuevos_dias};COUNT=12"]
        }
        # Actualizar el evento
        updated_event = service.events().patch(calendarId='primary', eventId=id, body=update_data).execute()
        print('Evento actualizado:', updated_event.get('recurrence'))

    def eliminar(id): #eliminar evento 
        service.events().delete(calendarId='primary', eventId=id).execute()
        print('Evento eliminado:', id)

    def crear(apodos, op, f_inicial, dias, l_frases): #crear evento
        event = {
            "summary": f"¡A reciclar {apodos[op][:-1]}!",
            "location": "Santiago",
            "description": f"¡A despertar {apodos[op][:-1]}! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. {l_frases[random.randint(0, len(l_frases)-1)]}",
            "colorId": int(apodos[op][-1]),
            "start": {
                "date":  f_inicial, #"aaaa-mm-dd" #hay un error y es que está marcando este día como primero. Debe ser el primer domingo o el primer día siguiente
                "timeZone": "America/Santiago"
            },
            "end": {
                "date":  f_inicial,
                "timeZone": "America/Santiago"
            },
            "recurrence": [
                f"RRULE:FREQ=WEEKLY;BYDAY={dias};COUNT=12"
            ]
        }
        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Evento creado exitosamente: {event.get('htmlLink')}")
        return event['id']

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

    #creación token de acceso a cuenta google
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

    #variables formulario 2
    dias="WE,TH" #***FORMULARIO_DIASELEGIDOS como string. Si no funciona el string se mete a una lista y se pegan en un string y listo). / esto en un formulario posterior al de crear cuenta. / deben estar por orden? probar FR,MO
    opcion=1 #int del 0 al 3.
    datos_calendario=[dias, opcion]

    apodos=["Corazón4", "Amiguín1", "Cosita2", "Bombón3"] #🍑🍎🥦🍆
    d_actual=dt.datetime.now()
    fecha=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}" #2023-11-30

    #variables formulario
    nombre="Matias" #***FORMULARIO_NOMBRE***
    correo="correo1" #***FORMULARIO_CORREO***
    datos_usuario=[nombre, correo]

    try:
        service = build("calendar", "v3", credentials=creds)

        #crear evento
        evento_id = crear(apodos, opcion, fecha, dias, lista_frases)
        print(f"ID evento: {evento_id}")

        #guardar en base de datos la id del evento
        # evento_id = "BYUVbuvytUBpatatillasconludillas" #variable de ejemplo
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()

        cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
        ant=cur.fetchone()[0]

        cur.execute(f"UPDATE Recycle_usuario SET id_evento='{evento_id}' WHERE correo='{correo}'")

        cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
        nue=cur.fetchone()[0]

        print(f"Usuario {correo}: ID guardada: de '{ant}' -> '{nue}'")
        con.commit()
        con.close()

        # #modificar evento
        # evento_id = "2ck7tt6d3e1inkhfdlvh6b7k68"
        # new_dias="WE,SA"
        # modificar(evento_id, new_dias)

        # #eliminar evento
        # eliminar("2ck7tt6d3e1inkhfdlvh6b7k68")
        # con = sqlite3.connect("db.sqlite3")
        # cur = con.cursor()

        # cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
        # ant=cur.fetchone()[0]

        # cur.execute(f"UPDATE Recycle_usuario SET id_evento='NULL' WHERE correo='{correo}'")

        # cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE correo='{correo}'")
        # nue=cur.fetchone()[0]
        
        # print(f"Usuario {correo}: ID guardada: de '{ant}' -> '{nue}'")
        # con.commit()
        # con.close()

    except HttpError as error:
        print("Ha ocurrido un error: ", error)

if __name__ == "__main__":
    main()
