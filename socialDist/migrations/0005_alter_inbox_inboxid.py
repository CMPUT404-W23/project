# Generated by Django 4.1.7 on 2023-03-23 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialDist", "0004_alter_followrequest_sender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inbox",
            name="inboxID",
            field=models.CharField(
                default="", max_length=200, primary_key=True, serialize=False
            ),
        ),
    ]