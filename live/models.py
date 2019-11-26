from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Feature(models.Model):
    title = models.CharField(max_length=50, default="Untitled Feature")
    slug = models.SlugField(max_length=50, default="untitled-feature")
    turn_duration = models.DurationField(default=timedelta(minutes=2))
    current_guests = ArrayField(
        models.CharField(max_length=100), default=list, blank=True
    )

    def __str__(self):
        return f"{self.title}"


class MediaPlayer(models.Model):
    channel_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.channel_name


# class Producer(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name="role", on_delete=models.CASCADE
#     )


# class Guest(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name="role", on_delete=models.CASCADE
#     )
#     feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
#     channel_names = ArrayField(models.CharField(max_length=100), blank=True)

#     class Meta:
#         ordering = ["headline"]
