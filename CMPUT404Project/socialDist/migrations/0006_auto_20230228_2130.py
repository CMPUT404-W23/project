# Generated by Django 3.1.6 on 2023-03-01 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0005_auto_20230228_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='authorId',
            new_name='id',
        ),
    ]
