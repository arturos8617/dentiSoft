# core/migrations/0002_create_default_entities.py
from django.db import migrations

def create_defaults(apps, schema_editor):
    Rol = apps.get_model("core", "Rol")
    Clinica = apps.get_model("core", "Clinica")

    # Crea o recupera el rol "CCA"
    Rol.objects.get_or_create(
        nombre="CCA",
        defaults={"descripcion": "Chief Clinic Administrator"}
    )

    # Crea o recupera la clínica "Default Clinic"
    Clinica.objects.get_or_create(
        nombre="Default Clinic",
        defaults={
            "direccion": "Dirección por defecto",
            "telefono": "",
            "email": ""
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_defaults, reverse_code=migrations.RunPython.noop),
    ]
