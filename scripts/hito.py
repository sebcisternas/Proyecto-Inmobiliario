
import os
import django

# Establecer la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectofinal.settings')

# Inicializar Django
django.setup()


from inmobilapp.models import Region, Inmueble, Comuna




# Obtener todas las regiones
regiones = Region.objects.all()

# Abrir el archivo de texto para escribir los resultados
with open('inmuebles_por_region.txt', 'w') as file:
    # Iterar sobre cada región
    for region in regiones:
        # Obtener las comunas dentro de la región actual
        comunas = region.comunas.all()
        # Escribir el nombre de la región en el archivo
        file.write(f'Region: {region.nombre}\n')
        # Iterar sobre cada comuna y obtener los inmuebles disponibles en ella
        for comuna in comunas:
            # Obtener los inmuebles disponibles en la comuna actual
            inmuebles = Inmueble.objects.filter(comuna=comuna, disponible=True)
            # Iterar sobre los inmuebles y escribir el nombre y la descripción en el archivo
            
            for inmueble in inmuebles:
                    file.write(f'           Nombre: {inmueble.nombre}\n')
                    file.write(f'           Descripción: {inmueble.descripcion}\n')
                    file.write(f'--------------------------------------------')
                    file.write('\n')  # Agregar línea en blanco entre regiones
        
comunas = Comuna.objects.all()

# Abrir el archivo de texto para escribir los resultados
with open('inmuebles_por_comuna.txt', 'w') as file:
    # Iterar sobre cada comuna
    for comuna in comunas:
        # Obtener los inmuebles disponibles en la comuna actual
        inmuebles = Inmueble.objects.filter(comuna=comuna, disponible=True)
        # Escribir el nombre de la comuna en el archivo
        # Iterar sobre los inmuebles y escribir el nombre y la descripción en el archivo
        file.write(f'Comuna: {comuna.nombre}\n')
        for inmueble in inmuebles:
                file.write(f'           Nombre: {inmueble.nombre}\n')
                file.write(f'           Descripción: {inmueble.descripcion}\n')
                file.write(f'--------------------------------------------')
                file.write('\n')  # Agregar línea en blanco entre comunas