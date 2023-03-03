# Generated by Django 3.1.6 on 2023-03-01 04:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0007_author_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commentID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='parentPostID',
            new_name='parentPost',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='postID',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='isLiked',
        ),
    ]
