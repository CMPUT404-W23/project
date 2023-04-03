# Generated by Django 4.1.7 on 2023-04-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialDist', '0002_rename_content_comment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='inboxID',
            field=models.CharField(default='', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='like',
            name='likeType',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('VISIBLE', 'Public'), ('FRIENDS', 'Private')], max_length=50),
        ),
    ]