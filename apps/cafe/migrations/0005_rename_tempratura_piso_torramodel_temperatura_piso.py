# Generated by Django 5.0.1 on 2024-03-02 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_torramodel_observacoes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='torramodel',
            old_name='tempratura_piso',
            new_name='temperatura_piso',
        ),
    ]
