from django import forms 
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    nombre = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, strip=False, widget=forms.PasswordInput, required=True)
    conf_contrasena = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Confirmar contraseña', required=False)
    
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'username',  #correo (debe llamarse username para iniciar sesion correctamente)
            'password',
            'conf_contrasena',
        ]

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        password = cleaned_data.get("password")
        conf_contrasena = cleaned_data.get("conf_contrasena")
        
        #if nombre=="":
            #conf_contrasena = cleaned_data.get("password")
        if password != conf_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden, vuelve a intentar.")  
        
 

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)        
            