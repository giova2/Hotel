# Generated by Django 3.0.5 on 2020-04-28 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitacion', '0011_auto_20200428_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'PENDIENTE'), ('Aprobada', 'APROBADA'), ('Cancelada', 'CANCELADA')], max_length=20),
        ),
    ]
