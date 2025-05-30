import os
import django

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CER2_GALLARDOMARTIN.settings')
django.setup()

from core.models import MaterialType

materiales = [
    {"codigo": "PAP", "nombre": "Papel y cartón"},
    {"codigo": "PLAS", "nombre": "Plásticos reciclables"},
    {"codigo": "VID", "nombre": "Vidrios"},
    {"codigo": "LAT", "nombre": "Latas"},
    {"codigo": "ELEC", "nombre": "Electrónicos pequeños"},
    {"codigo": "TEX", "nombre": "Textiles"},
    {"codigo": "VOL", "nombre": "Voluminosos reciclables"},
]

for mat in materiales:
    obj, creado = MaterialType.objects.get_or_create(
        codigo=mat["codigo"],
        defaults={"nombre": mat["nombre"], "descripcion": ""}
    )
    if creado:
        print(f"✅ Material agregado: {mat['nombre']}")
    else:
        print(f"⚠️ Ya existía: {mat['nombre']}")
