# Generated by Django 5.2 on 2025-05-30 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('en_ruta', 'En ruta'), ('completada', 'Completada')], default='pendiente', max_length=20),
        ),
    ]
