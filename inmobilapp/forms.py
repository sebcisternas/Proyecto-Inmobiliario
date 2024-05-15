from django import forms
from .models import Usuario, SolicitudArriendo,Inmueble
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name','email','rut', 'direccion', 'telefono', 'tipo_usuario')
       
        
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ('propietario',)  # Excluimos el campo 'propietario' del formulario       
        
        
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = ['first_name', 'last_name', 'email','direccion','telefono']
