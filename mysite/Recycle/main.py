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

def comprobacion(correo): #comprobaremos si el correo tiene un evento ya creado.
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
    id_evento=cur.fetchone()[0]

    con.commit()
    con.close()

    if id_evento!='NULL' and id_evento!='a' and id_evento!=0:
        return True
    else:
        return False

def main(accion, dias, opcion, correo):
    
    #declaración funciones
    def modificar(id, nuevos_dias, op, l_frases): #actualizar evento 
        # Datos a actualizar
        update_data = {
            "summary": f"¡A reciclar {apodos[op][:-1]}!",
            "location": "Santiago",
            "description": f"¡A despertar {apodos[op][:-1]}! Hoy es día de reciclaje. No puedes desaprovechar la oportunidad. {l_frases[random.randint(0, len(l_frases)-1)]}",
            'colorId': int(apodos[op][-1]),
            'recurrence': [f"RRULE:FREQ=WEEKLY;BYDAY={nuevos_dias};COUNT=12"]
        }
        # Actualizar el evento
        updated_event = service.events().patch(calendarId='primary', eventId=id, body=update_data).execute()
        print('¡Evento modificado correctamente!')

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

    accion=accion
    dias=dias
    opcion=opcion
    correo=correo

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
            flow = InstalledAppFlow.from_client_secrets_file("Recycle\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    apodos=["Corazón4", "Amiguín1", "Cosita2", "Bombón3"] #🍑🍎🥦🍆
    d_actual=dt.datetime.now()
    fecha=f"{d_actual.strftime('%Y')}-{d_actual.strftime('%m')}-{d_actual.strftime('%d')}"

    try:
        service = build("calendar", "v3", credentials=creds)

        if accion=='crear':
            if comprobacion(correo)==False:
                #crear evento
                evento_id = crear(apodos, opcion, fecha, dias, lista_frases)
                print(f"ID evento: {evento_id}")

                #guardar en base de datos la id del evento
                con = sqlite3.connect("db.sqlite3")
                cur = con.cursor()

                cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
                ant=cur.fetchone()[0]

                cur.execute(f"UPDATE Recycle_usuario SET id_evento='{evento_id}' WHERE username='{correo}'")

                cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
                nue=cur.fetchone()[0]

                print(f"Usuario {correo}: ID guardada: de '{ant}' -> '{nue}'")
                con.commit()
                con.close()
            elif comprobacion(correo)==True:
                print('Ya tienes un evento existente. Modifícalo o elimínalo antes de crear uno nuevo.')

        elif accion=='modificar':
            #modificar evento
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()

            cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
            evento_id_ant=cur.fetchone()[0]

            if comprobacion(correo)==True:
                modificar(evento_id_ant, dias, opcion, lista_frases)
            else:
                print('No hay un evento para modificar')

            cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
            evento_id_nue=cur.fetchone()[0]

            con.commit()
            con.close()
            
            print(f"Usuario {correo}: ID guardada: de '{evento_id_ant}' -> '{evento_id_nue}'")

        elif accion=='eliminar':
            #eliminar evento
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()

            cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
            evento_id_an=cur.fetchone()[0]

            eliminar(evento_id_an)

            cur.execute(f"UPDATE Recycle_usuario SET id_evento='NULL' WHERE username='{correo}'")

            cur.execute(f"SELECT id_evento FROM Recycle_usuario WHERE username='{correo}'")
            evento_id_nu=cur.fetchone()[0]
            
            print(f"Usuario {correo}: ID guardada: de '{evento_id_an}' -> '{evento_id_nu}'")
            con.commit()
            con.close()
        
        print('--- Acción completada correctamente ---')

    except HttpError as error:
        print("Ha ocurrido un error: ", error)

if __name__ == "__main__":
    main()
