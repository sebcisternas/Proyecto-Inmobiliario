from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Usuario(User):
    
           
    TIPO_USUARIO_CHOISES = [
        ('arrendatario','Arrendatario'),
        ('arrendador','Arrendador'),
    ]
    
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    rut= models.CharField(max_length=10,unique=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=13)
    tipo_usuario = models.CharField(max_length=20,choices=TIPO_USUARIO_CHOISES)
    
    
        
    def __str__(self) -> str:
        return f"{self.nombre}{self.apellidos}"
    
    
class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOISES = [
        ('casa','Casa'),
        ('departamento','Departamento'),
        ('parcela','Parcela'),
    ]
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    m2_construidos = models.IntegerField()
    m2_terreno = models.IntegerField()
    habitaciones = models.IntegerField()
    banios = models.IntegerField()
    cant_estacionamientos = models.IntegerField()
    imagen = models.URLField(max_length=200)
    precio = models.IntegerField()
    comuna= models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    tipo_de_inmueble= models.CharField(max_length=20,choices=TIPO_INMUEBLE_CHOISES)
    
    def __str__(self) -> str:
        return f"{self.nombre}"