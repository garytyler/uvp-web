from django.conf import settings
from django.db import models


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="logged_in_user",
        on_delete=models.CASCADE,
    )


class MediaDisplayerClient(models.Model):
    channel_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.channel_name


class InteractorClient(models.Model):
    session_key = models.CharField(max_length=100, unique=True, blank=False)
    display_name = models.CharField(max_length=100, default="Anonymous")
    available = models.BooleanField(default=False)  # Has open socket

    def __str__(self):
        return f"{self.session_key}/{self.display_name}"
