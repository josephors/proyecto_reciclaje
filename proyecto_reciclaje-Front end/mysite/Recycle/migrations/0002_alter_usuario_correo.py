# Generated by Django 4.2.5 on 2023-11-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recycle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
