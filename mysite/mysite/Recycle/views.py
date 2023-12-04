from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UsuarioForm, UserLoginForm
from django.contrib.auth.models import User
from .models import Usuario



# Create your views here.



def NombreFuncion (request):
    return HttpResponse('<h1>Martin te chupo el pico</h1>')
def index (request):
    return render(request, 'index.html')

def Login (request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        idusername = Usuario.objects.get(username=usern)
        idpassword = Usuario.objects.get(password=passw)
        if idusername.id == idpassword.id:
            login(request, idusername)
            return redirect('pag2')
        else:
            messages.error(request, "Error de autenticación")
            return redirect('index')   
    return render(request, 'Login.html')     
def pag2 (request):
    return render(request, 'pag2.html')
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


     