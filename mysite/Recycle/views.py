from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UsuarioForm


# Create your views here.


def signup(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada correctamente") 
            return redirect('Login')  # Redirige a la página de Login
    else:
        form = UsuarioForm()    
    return render(request, 'signup.html', {'form': form})    

def NombreFuncion (request):
    return HttpResponse('<h1>Martin te chupo el pico</h1>')
def index (request):
    return render(request, 'index.html')
def Login (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pag2')  # Redirige a la página de bienvenida
    else:
        form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form})
def pag2 (request):
    return render(request, 'pag2.html')
def funciones (request):
    return render(request, 'funciones.html')

