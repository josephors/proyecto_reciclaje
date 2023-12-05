from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import UsuarioForm, UserLoginForm
from django.contrib.auth.models import User
from .models import Usuario



# Create your views here.



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

