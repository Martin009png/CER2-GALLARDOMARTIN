# Generated by Django 5.2 on 2025-05-30 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_puntolimpio_recomendacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='fecha_completada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
