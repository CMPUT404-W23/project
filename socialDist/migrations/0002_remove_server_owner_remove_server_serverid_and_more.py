<<<<<<< HEAD
# Generated by Django 4.1.7 on 2023-03-18 18:37
=======
# Generated by Django 4.1.7 on 2023-03-15 02:26
>>>>>>> origin/dev

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('socialDist', '0001_initial'),
=======
        ("socialDist", "0001_initial"),
>>>>>>> origin/dev
    ]

    operations = [
        migrations.RemoveField(
<<<<<<< HEAD
            model_name='server',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='server',
            name='serverID',
        ),
        migrations.RemoveField(
            model_name='server',
            name='serverName',
        ),
        migrations.AddField(
            model_name='server',
            name='serverAddress',
            field=models.URLField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.TextField(choices=[('text/plain', 'plaintext'), ('text/markdown', 'markdown')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.TextField(choices=[('text/plain', 'plaintext'), ('text/markdown', 'markdown'), ('application/base64', 'binary'), ('image/png;base64', 'PNG image'), ('image/jpeg;base64', 'JPEG image')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('VISIBLE', 'Public'), ('FRIENDS', 'Private')], max_length=30),
=======
            model_name="server",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="server",
            name="serverID",
        ),
        migrations.RemoveField(
            model_name="server",
            name="serverName",
        ),
        migrations.AddField(
            model_name="server",
            name="serverAddress",
            field=models.URLField(
                default="localhost", primary_key=True, serialize=False
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comment",
            name="contentType",
            field=models.TextField(
                choices=[("text/plain", "plaintext"), ("text/markdown", "markdown")]
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="contentType",
            field=models.TextField(
                choices=[
                    ("text/plain", "plaintext"),
                    ("text/markdown", "markdown"),
                    ("application/base64", "binary"),
                    ("image/png;base64", "PNG image"),
                    ("image/jpeg;base64", "JPEG image"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="visibility",
            field=models.CharField(
                choices=[("VISIBLE", "Public"), ("FRIENDS", "Private")], max_length=30
            ),
>>>>>>> origin/dev
        ),
    ]
