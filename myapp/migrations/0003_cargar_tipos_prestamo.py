from django.db import migrations

TIPOS_PRESTAMO = [
    ('Préstamo de Emergencia', 0),
    ('Préstamo Personal',      5),
    ('Préstamo de Salud',      3),
    ('Préstamo de Educación',  4),
    ('Préstamo de Vivienda',   8),
    ('Préstamo de Vehículo',   7),
]

def cargar_tipos(apps, schema_editor):
    TipoPrestamo = apps.get_model('myapp', 'TipoPrestamo')
    for nombre, tasa in TIPOS_PRESTAMO:
        TipoPrestamo.objects.get_or_create(tipo_prestamo=nombre, defaults={'tasa_de_interes': tasa})

def eliminar_tipos(apps, schema_editor):
    TipoPrestamo = apps.get_model('myapp', 'TipoPrestamo')
    TipoPrestamo.objects.filter(tipo_prestamo__in=[t[0] for t in TIPOS_PRESTAMO]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_cargar_comunas_santiago'),
    ]

    operations = [
        migrations.RunPython(cargar_tipos, eliminar_tipos),
    ]
