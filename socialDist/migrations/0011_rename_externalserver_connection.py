# Generated by Django 4.1.7 on 2023-03-21 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0010_rename_connection_externalserver'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExternalServer',
            new_name='Connection',
        ),
    ]
