# Generated by Django 4.1.7 on 2023-04-02 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
    ]