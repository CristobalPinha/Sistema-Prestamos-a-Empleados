from django.db import migrations

COMUNAS_SANTIAGO = [
    'Cerrillos', 'Cerro Navia', 'Conchalí', 'El Bosque', 'Estación Central',
    'Huechuraba', 'Independencia', 'La Cisterna', 'La Florida', 'La Granja',
    'La Pintana', 'La Reina', 'Las Condes', 'Lo Barnechea', 'Lo Espejo',
    'Lo Prado', 'Macul', 'Maipú', 'Ñuñoa', 'Pedro Aguirre Cerda',
    'Peñalolén', 'Providencia', 'Pudahuel', 'Quilicura', 'Quinta Normal',
    'Recoleta', 'Renca', 'San Joaquín', 'San Miguel', 'San Ramón',
    'Santiago', 'Vitacura', 'Puente Alto', 'San Bernardo', 'Padre Hurtado',
]

def cargar_comunas(apps, schema_editor):
    Comuna = apps.get_model('myapp', 'Comuna')
    for nombre in COMUNAS_SANTIAGO:
        Comuna.objects.get_or_create(nombre_comuna=nombre)

def eliminar_comunas(apps, schema_editor):
    Comuna = apps.get_model('myapp', 'Comuna')
    Comuna.objects.filter(nombre_comuna__in=COMUNAS_SANTIAGO).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_comunas, eliminar_comunas),
    ]
