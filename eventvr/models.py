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
