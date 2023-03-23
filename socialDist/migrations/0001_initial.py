# Generated by Django 4.1.7 on 2023-03-22 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("host", models.CharField(max_length=200)),
                ("displayName", models.CharField(default="", max_length=40)),
                ("github", models.URLField(blank=True, null=True)),
                ("profileImage", models.URLField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("published", models.DateTimeField(auto_created=True)),
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("content", models.TextField()),
                (
                    "contentType",
                    models.TextField(
                        choices=[
                            ("text/plain", "plaintext"),
                            ("text/markdown", "markdown"),
                        ]
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="socialDist.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Connection",
            fields=[
                ("apiAddress", models.URLField(primary_key=True, serialize=False)),
                ("apiCreds", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Server",
            fields=[
                ("serverAddress", models.URLField(primary_key=True, serialize=False)),
                ("serverKey", models.TextField(blank=True)),
                ("isLocalServer", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("published", models.DateTimeField(auto_created=True)),
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=50)),
                ("source", models.CharField(max_length=50)),
                ("origin", models.CharField(max_length=50)),
                ("description", models.TextField()),
                (
                    "contentType",
                    models.TextField(
                        choices=[
                            ("text/plain", "plaintext"),
                            ("text/markdown", "markdown"),
                            ("application/base64", "binary"),
                            ("image/png;base64", "PNG image"),
                            ("image/jpeg;base64", "JPEG image"),
                            ("image/jpg;base64", "JPG image"),
                        ]
                    ),
                ),
                ("content", models.TextField()),
                ("categories", models.CharField(max_length=100)),
                (
                    "visibility",
                    models.CharField(
                        choices=[("VISIBLE", "Public"), ("FRIENDS", "Private")],
                        max_length=30,
                    ),
                ),
                ("unlisted", models.BooleanField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="socialDist.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                ("published", models.DateTimeField(auto_created=True)),
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("summary", models.TextField()),
                ("likeType", models.CharField(max_length=20)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked",
                        to="socialDist.author",
                    ),
                ),
                (
                    "parentComment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="socialDist.comment",
                    ),
                ),
                (
                    "parentPost",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="socialDist.post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Inbox",
            fields=[
                (
                    "inboxID",
                    models.CharField(
                        default="", max_length=40, primary_key=True, serialize=False
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialDist.author",
                    ),
                ),
                ("posts", models.ManyToManyField(to="socialDist.post")),
            ],
        ),
        migrations.CreateModel(
            name="FollowRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_created=True)),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="send_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recievced_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="parentPost",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="socialDist.post",
            ),
        ),
        migrations.CreateModel(
            name="UserFollowing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to="socialDist.author",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to="socialDist.author",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_id", "following_user_id")},
            },
        ),
    ]
