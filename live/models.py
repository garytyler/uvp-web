from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify

from .caching import CachedListSet


class Feature(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", max_length=100, editable=False)
    turn_duration = models.DurationField(default=timedelta(minutes=2))
    current_guests = ArrayField(
        models.CharField(max_length=100), default=list, blank=True
    )
    channel_name = models.CharField(max_length=200, blank=True)

    # class Meta:
    #     unique_together = [['user', 'slug']] # Set when users are added

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @cached_property
    def cache_key_prefix(self):
        return f"{self.pk}:{self.slug}:"

    @property
    def guest_queue(self):
        return CachedListSet(self.cache_key_prefix + "guest_queue")


# class MediaPlayer(models.Model):
#     channel_name = models.CharField(max_length=200, blank=True)
#     feature = models.ForeignKey("Feature", on_delete=models.CASCADE,)

#     def __str__(self):
#         return self.channel_name


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
