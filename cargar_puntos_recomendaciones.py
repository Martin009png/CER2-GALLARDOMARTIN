import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CER2_GALLARDOMARTIN.settings')
django.setup()

from core.models import PuntoLimpio, Recomendacion

# Datos para puntos limpios
puntos = [
    {
        "nombre": "Centro de Acopio Comunal",
        "direccion": "Av. Principal 123, Comuna",
        "horario": "Lunes a viernes de 9:00 a 17:00"
    },
    {
        "nombre": "Punto Limpio Parque Central",
        "direccion": "Parque Central, sector sur",
        "horario": "Todos los días de 8:00 a 20:00"
    },
    # Puedes agregar más aquí
]

# Datos para recomendaciones
recomendaciones = [
    {
        "titulo": "Separa tus residuos",
        "texto": "Separa papel, plástico, vidrio y orgánicos para facilitar el reciclaje."
    },
    {
        "titulo": "Limpia los materiales",
        "texto": "Asegúrate de lavar y secar los envases antes de reciclarlos."
    },
    # Puedes agregar más aquí
]

# Insertar puntos limpios
for punto in puntos:
    obj, creado = PuntoLimpio.objects.get_or_create(
        nombre=punto["nombre"],
        defaults={
            "direccion": punto["direccion"],
            "horario": punto["horario"]
        }
    )
    if creado:
        print(f"✅ Punto limpio agregado: {punto['nombre']}")
    else:
        print(f"⚠️ Ya existía: {punto['nombre']}")

# Insertar recomendaciones
for reco in recomendaciones:
    obj, creado = Recomendacion.objects.get_or_create(
        titulo=reco["titulo"],
        defaults={
            "texto": reco["texto"]
        }
    )
    if creado:
        print(f"✅ Recomendación agregada: {reco['titulo']}")
    else:
        print(f"⚠️ Ya existía: {reco['titulo']}")
