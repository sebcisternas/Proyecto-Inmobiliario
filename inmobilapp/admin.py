from django.contrib import admin
from .models import Usuario, Inmueble, SolicitudArriendo,Region,Comuna
from django.contrib.auth.admin import UserAdmin, User
from .forms import RegistroUsuarioForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = RegistroUsuarioForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ['username', 'first_name', 'last_name', 'password','email', 'rut', 'direccion', 'telefono', 'tipo_usuario',]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ('rut', 'direccion', 'telefono', 'tipo_usuario')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ('rut', 'direccion', 'telefono', 'tipo_usuario')}),)

admin.site.register(Usuario, CustomUserAdmin)


admin.site.register(Inmueble)
admin.site.register(SolicitudArriendo)
admin.site.register(Region)
admin.site.register(Comuna)