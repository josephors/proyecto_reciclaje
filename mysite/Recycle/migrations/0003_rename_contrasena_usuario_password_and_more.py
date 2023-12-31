# Generated by Django 4.2.5 on 2023-12-04 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recycle', '0002_alter_usuario_correo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='contrasena',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='correo',
            new_name='username',
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
