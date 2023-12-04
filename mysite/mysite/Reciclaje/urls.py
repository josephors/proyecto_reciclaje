"""
URL configuration for Reciclaje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Recycle import views
from Recycle.views import signup

urlpatterns = [
    path('Ejemplo/', views.NombreFuncion),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('Login/', views.Login, name='Login'),
    path('pag2/', views.pag2, name='pag2'),
    path('funciones/', views.funciones, name='funciones'),
    path('signup/', signup, name='signup'),
]
