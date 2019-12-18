from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models
from django.utils.text import slugify

from .caching import CachedListSet


class Feature(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", max_length=100, editable=False)
    turn_duration = models.DurationField(default=timedelta(minutes=2))
    current_guests = ArrayField(
        models.CharField(max_length=100), default=list, blank=True
    )

    # class Meta:
    #     unique_together = [['user', 'slug']] # Set when users are added

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def cache_key_prefix(self):
        return f"{self.pk}:{self.slug}:"

    @property
    def guest_queue(self):
        return CachedListSet(self.cache_key_prefix + "guest_queue")

    @property
    def presenter_channel(self):
        return cache.get(self.cache_key_prefix + "presenter_channel")

    @presenter_channel.setter
    def presenter_channel(self, value):
        return cache.set(self.cache_key_prefix + "presenter_channel", value)
