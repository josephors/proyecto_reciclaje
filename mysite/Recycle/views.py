from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import UsuarioForm, UserLoginForm
from django.contrib.auth.models import User
from .models import Usuario
from .main import main
from .main import comprobacion



def NombreFuncion (request):
    return HttpResponse('<h1>Martin te chupo el pico</h1>')
def index (request):
    idusername = request.session.get('idusername')
    variable=False
    if idusername is not None:
        variable=True
    return render(request, 'index.html', {'variable' : variable})
def Login (request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        print(usern, passw)
        try:
            idusername = Usuario.objects.get(username=usern)
        except Usuario.DoesNotExist:
            messages.error(request, "Error de autenticación")
            return redirect('Login')
        try:
            idpassword = Usuario.objects.get(password=passw)
        except Usuario.DoesNotExist:
            messages.error(request, "Error de autenticación")
            return redirect('Login')
        print(idusername, idpassword)
        if idusername.id == idpassword.id:
            login(request, idusername)
            request.session['idusername'] = idusername.id
            return redirect('pag2')
        else:
            messages.error(request, "Error de autenticación")
            return redirect('Login')   
    return render(request, 'Login.html')     
def pag2 (request):
    idusername = request.session.get('idusername')
    print("hola")
    print(idusername)
    if idusername is not None:
        try:
            # Recuperar el usuario completo usando la id
            user_instance = Usuario.objects.get(id=idusername)

            # Obtener el nombre y el correo del usuario
            nombre_usuario = user_instance.nombre
            correo_usuario = user_instance.username

            context = {
                'nombre_usuario': nombre_usuario,
                'correo_usuario': correo_usuario,
            }
            return render(request, 'pag2.html', context)
        except Usuario.DoesNotExist:
            messages.error(request, "Porfavor inicia sesión antes")
            return redirect('Login')
    else:
        messages.error(request, "Porfavor inicia sesión antes")
        return redirect('Login')
def funciones (request):
    return render(request, 'funciones.html')

def formulario2(request):
    if request.method=='POST':
        formulario = request.POST
        accion=formulario['accion'].lower()
        correo=formulario['username'] #debe ser gmail y el de la sesión creada

        dias_form=[]
        dias=""
        opcion=99

        if accion=='crear' or (accion=='modificar' and comprobacion(correo)==True):
            if len(formulario)>=5:
                dias_form=formulario.getlist('dias')
                for d in dias_form:
                    dias+=d+','
                dias=dias[:-1]

                opcion=int(formulario['opcion'])

                main(accion, dias, opcion, correo)
            else:
                print('Debes rellenar todas las casillas.')
        elif accion=='eliminar':
            if comprobacion(correo)==True:
                main(accion, dias, opcion, correo)
            elif comprobacion(correo)==False:
                print('No hay un evento para eliminar.')

    return render(request, 'formulario2.html')

def signup(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid() and form.data['password'] == form.data['conf_contrasena']:
            user = form.save()
            messages.success(request, "Cuenta creada correctamente") 
            return redirect('Login')  # Redirige a la página de Login
    else:
        form = UsuarioForm()  
    return render(request, 'signup.html', {'form': form})    

def signout(request):
    logout(request)
    variable = False
    return redirect("index")




# #PROBLEMAS PENDIENTES FORMULARIO2
#tenemos el error de que si no se rellena alguna casilla y se apreta crear o modificar, nos vamos a la chucha. ojo.
    #-una solución es que solo se ejecuten si están todas las casillas rellenadas
#qué pasa si no se rellena el correo? resp: la pagina te obliga a poner el correo, sino no funciona el boton y solo te sale un mensaje q dice "debes rellenar esto"
#qué pasa si metemos un correo incorrecto?
#hay que pasar los mensajes de la consola al html si es posible (los fundamentales)

#crear necesita correo, dias, opcion
#modificar necesita correo, dias, opcion
#eliminar necesita correo