# Generated by Django 5.1.2 on 2025-06-26 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_perfil_estoy_buscando_perfil_experiencia_laboral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='estoy_buscando',
            field=models.CharField(blank=True, choices=[('pasantia', 'Práctica y/o pasantía'), ('trabajo', 'Trabajo')], max_length=20),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='experiencia_laboral',
            field=models.CharField(blank=True, choices=[('sin_exp', 'Sin experiencia'), ('1_ano', '1 año'), ('2_anos', '2 años')], max_length=20),
        ),
    ]
