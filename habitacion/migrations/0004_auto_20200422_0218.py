# Generated by Django 3.0.5 on 2020-04-22 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitacion', '0003_auto_20200421_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageneshabitacion',
            old_name='habitacion_id',
            new_name='habitacion',
        ),
        migrations.RenameField(
            model_name='reservas',
            old_name='habitacion_id',
            new_name='habitacion',
        ),
        migrations.AlterField(
            model_name='habitacion',
            name='servicios',
            field=models.CharField(choices=[('COCINA', 'Cocina'), ('AIRE_CONDICIONADO', 'Aire condicioado'), ('DUCHA', 'Ducha'), ('WIFI', 'Wifi'), ('TOALLAS', 'Toallas')], max_length=20),
        ),
    ]
