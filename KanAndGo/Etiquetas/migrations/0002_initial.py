# Generated by Django 5.1.7 on 2025-03-13 00:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Etiquetas', '0001_initial'),
        ('Tareas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleetiqueta',
            name='tarea_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tareas.tarea', verbose_name='Tarea'),
        ),
    ]
