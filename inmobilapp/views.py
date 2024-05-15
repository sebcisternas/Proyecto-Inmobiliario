from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from inmobilapp.models import SolicitudArriendo, Inmueble, Usuario ,Region,Comuna
from .forms import RegistroUsuarioForm, SolicitudArriendoForm, InmuebleForm,CustomUserChangeForm
from django.http import JsonResponse

def index(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'index.html', {'inmuebles': inmuebles})


def about(request):
    return render(request, 'about.html')

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    if region_id:
        comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
        return JsonResponse({'comunas': list(comunas)})
    else:
        return JsonResponse({'comunas': []})

@login_required
def propiedades(request):
    
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para acceder a las propiedades.')
        return redirect('login')  # Cambia 'login' al nombre de la URL de tu página de inicio de sesión

    solicitudes = SolicitudArriendo.objects.filter(arrendatario=request.user)
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    inmuebles = Inmueble.objects.all()
    if region_id:
        inmuebles = inmuebles.filter(comuna__region_id=region_id)
    if comuna_id:
        inmuebles = inmuebles.filter(comuna_id=comuna_id)
    
    form_solicitud = SolicitudArriendoForm(request.POST or None)  # Instancia del formulario de solicitud

    if request.method == 'POST':
        if form_solicitud.is_valid():
            inmueble_id = request.POST.get('inmueble_id')
            inmueble = get_object_or_404(Inmueble, pk=inmueble_id)
            solicitud = form_solicitud.save(commit=False)
            solicitud.arrendatario = request.user
            solicitud.inmueble = inmueble
            solicitud.save()
            messages.success(request, 'Solicitud enviada con éxito')
            return redirect('propiedades')

    return render(request, 'propiedades.html', {'solicitudes': solicitudes, 'regiones': regiones, 'comunas': comunas, 'inmuebles': inmuebles, 'form_solicitud': form_solicitud})
   


@login_required
def detalle_inmueble(request, id):
    inmueble = Inmueble.objects.get(pk=id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            user= authenticate(username=form.cleaned_data["username"],password=form.cleaned_data["password1"])
            login(request,user)
            messages.success(request, 'Registro Exitoso')
            return redirect('index')  # Redirigir al usuario después del registro exitoso
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro_usuario.html', {'form': form})


@login_required
def generar_solicitud_arriendo(request, id):
    inmueble = get_object_or_404(Inmueble, pk=id)
    if request.user.is_authenticated and request.user.tipo_usuario == 'arrendatario':
        if request.method == 'POST':
            form = SolicitudArriendoForm(request.POST)
            if form.is_valid():
                solicitud = form.save(commit=False)
                solicitud.arrendatario = request.user
                solicitud.inmueble = inmueble
                solicitud.save()
                return redirect('detalle', id=inmueble.id)
        else:
            form = SolicitudArriendoForm()
        return render(request, 'generar_solicitud_arriendo.html', {'form': form, 'inmueble': inmueble})
    else:
        return redirect('index')
    
    
@login_required
def solicitudes_arrendador(request):
    if request.user.tipo_usuario == 'arrendador':
        solicitudes = SolicitudArriendo.objects.filter(inmueble__propietario=request.user)
        return render(request, 'solicitudes_arrendador.html', {'solicitudes': solicitudes})
    else:
        return redirect('index')

@login_required
def alta_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user
            inmueble.save()
            messages.success(request, 'Inmueble Creado con Exito')
            return redirect('detalle', id=inmueble.id)
    else:
        form = InmuebleForm()
    return render(request, 'alta_inmueble.html', {'form': form})



@login_required
def actualizar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, pk=id)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actualizacion Exitosa')
            return redirect('dashboard')
    else:
        form = InmuebleForm(instance=inmueble)
    return render(request, 'editar_inmueble.html',{'form':form })


def eliminar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, pk=id)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('dashboard')
    else:
        return render(request,'eliminar_inmueble.html', {'inmueble':inmueble} )
        
        
@login_required
def dashboard(request):
    if request.user.tipo_usuario == 'arrendatario':
        solicitudes = SolicitudArriendo.objects.filter(arrendatario=request.user)
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()
        region_id = request.GET.get('region')
        comuna_id = request.GET.get('comuna')
        inmuebles = Inmueble.objects.all()
        if region_id:
            inmuebles = inmuebles.filter(comuna__region_id=region_id)
        if comuna_id:
            inmuebles = inmuebles.filter(comuna_id=comuna_id)
        
        return render(request, 'dashboard_arrendatario.html', {'solicitudes': solicitudes, 'regiones': regiones, 'comunas': comunas, 'inmuebles': inmuebles})
    
    elif request.user.tipo_usuario == 'arrendador':
        # Obtener las solicitudes recibidas por el arrendador
        solicitudes_recibidas = SolicitudArriendo.objects.filter(inmueble__propietario=request.user)
        # Obtener los inmuebles del arrendador
        inmuebles = Inmueble.objects.filter(propietario=request.user)
        return render(request, 'dashboard_arrendador.html', {'solicitudes_recibidas': solicitudes_recibidas, 'inmuebles': inmuebles})

@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Los datos del usuario han sido actualizados!')
            return redirect('index') 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'perfil.html', {'form': form})

   
    
@login_required
def cambiar_estado_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArriendo, pk=solicitud_id)
    if solicitud.inmueble.propietario == request.user :
        if request.method == 'POST':
            nuevo_estado = request.POST.get('nuevo_estado')
            solicitud.estado = nuevo_estado
            solicitud.save()
    return redirect('dashboard')