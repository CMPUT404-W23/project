# Generated by Django 3.1.6 on 2023-03-01 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0009_auto_20230228_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='dateTime',
            new_name='published',
        ),
    ]