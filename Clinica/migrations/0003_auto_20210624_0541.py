# Generated by Django 3.1.7 on 2021-06-24 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Clinica', '0002_auto_20210624_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='Expedientepaciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clinica.expedientepaciente', verbose_name='Paciente'),
        ),
    ]