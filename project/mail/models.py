from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user: Any = models.ManyToManyField(User, related_name="users")
    name = models.TextField()
    last_name = models.TextField(blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    about_self = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_inform = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        blank=True,
        null=True,
        default="photos/2023/03/18/Anonimus1.webp",
    )
    live_place = models.TextField(blank=True, null=True)

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, verbose_name="уникальный URL", db_index=True)
    friend = models.ManyToManyField("profile", related_name="friends")
    request_to_friend = models.ManyToManyField("profile", related_name="requests")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profile", kwargs={"profile_slug": self.slug})

    class Meta:
        verbose_name = "Профили"
        verbose_name_plural = "Профили"
        ordering = ["name", "time_create"]


class Chat(models.Model):
    profile = models.ManyToManyField(Profile, related_name="profiles")
    hidden = models.BooleanField(default=0)
    chat_name = models.TextField()
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, verbose_name="URL")

    def __str__(self):
        return self.chat_name

    def get_absolute_url(self):
        return reverse("chat", kwargs={"chat_slug": self.slug})

    class Meta:
        verbose_name = "Чаты"
        verbose_name_plural = "Чаты"
        ordering = ["time_update", "chat_name"]


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    text = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=0)
    hidden = models.BooleanField(default=0)
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING)
    attached_file = models.FileField(upload_to="documents/%Y/%m/%d/", blank=True)
    attached_photo = models.FileField(upload_to="attached_photo/%Y/%m/%d/", blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщения"
        ordering = ["send_time", "sender"]


class ActiveProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    act = models.IntegerField()
