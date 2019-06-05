from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="logged_in_user",
        on_delete=models.CASCADE,
    )


class MediaPlayer(models.Model):
    channel_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.channel_name


class Guest(models.Model):
    session_key = models.CharField(max_length=100, unique=True, blank=False)
    display_name = models.CharField(max_length=100, default="Anonymous Guest")
    available = models.BooleanField(default=False)
    channel_names = ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return f"{self.session_key}|{self.display_name}"


class Feature(models.Model):
    title = models.CharField(max_length=100, default="Unnamed Feature")
    guest_queue = ArrayField(models.CharField(max_length=100), default=list, blank=True)

    def __str__(self):
        return f"{self.title}"
