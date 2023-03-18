# Generated by Django 4.1.7 on 2023-03-18 19:25

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
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hidden", models.BooleanField(default=0)),
                ("chat_name", models.TextField()),
                ("time_update", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True, verbose_name="URL")),
            ],
            options={
                "verbose_name": "Чаты",
                "verbose_name_plural": "Чаты",
                "ordering": ["time_update", "chat_name"],
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("last_name", models.TextField(blank=True, null=True)),
                ("date_birth", models.DateField(blank=True, null=True)),
                ("about_self", models.TextField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("contact_inform", models.TextField(blank=True, null=True)),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        default="photos/2023/03/18/Anonimus1.webp",
                        null=True,
                        upload_to="photos/%Y/%m/%d/",
                    ),
                ),
                ("live_place", models.TextField(blank=True, null=True)),
                ("time_create", models.DateTimeField(auto_now_add=True)),
                ("time_update", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                ("slug", models.SlugField(unique=True, verbose_name="уникальный URL")),
                (
                    "friend",
                    models.ManyToManyField(related_name="friends", to="mail.profile"),
                ),
                (
                    "request_to_friend",
                    models.ManyToManyField(related_name="requests", to="mail.profile"),
                ),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="users", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Профили",
                "verbose_name_plural": "Профили",
                "ordering": ["name", "time_create"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("send_time", models.DateTimeField(auto_now_add=True)),
                ("read_status", models.BooleanField(default=0)),
                ("hidden", models.BooleanField(default=0)),
                (
                    "attached_file",
                    models.FileField(blank=True, upload_to="documents/%Y/%m/%d/"),
                ),
                (
                    "attached_photo",
                    models.FileField(blank=True, upload_to="attached_photo/%Y/%m/%d/"),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="mail.chat"
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="mail.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщения",
                "verbose_name_plural": "Сообщения",
                "ordering": ["send_time", "sender"],
            },
        ),
        migrations.AddField(
            model_name="chat",
            name="profile",
            field=models.ManyToManyField(related_name="profiles", to="mail.profile"),
        ),
        migrations.CreateModel(
            name="ActiveProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("act", models.IntegerField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]