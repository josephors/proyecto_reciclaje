# Proyecto Reciclaje:
Ecolendario. Aplicación para la organización de tus días de para reciclar mediante la interacción con la API de Google Cloud, autentificación de la cuenta de Google y Google Calendar.

## Requerimientos:
Instalar biblioteca cliente de Google para Python en directorio del virtual enviroment:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
o consultar última versión en: https://developers.google.com/calendar/api/quickstart/python

Es necesario, además, crear un proyecto de Google Cloud, a la vez que ubicar las credenciales respectivas en "...\Recycle\".

## Uso:
Habiendo terminado la instalación, iniciado el virtual enviroment y ubicados en "/mysite", podemos iniciar el servidor con el siguiente comando y la página estaría iniciada y funcional:
```
py manage.py runserver
```
