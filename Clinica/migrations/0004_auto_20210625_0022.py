# Generated by Django 3.1.7 on 2021-06-25 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Clinica', '0003_auto_20210624_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='Tratamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clinica.tratamiento', verbose_name='Tratamiento'),
        ),
    ]
