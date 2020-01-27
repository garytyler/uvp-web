from datetime import timedelta

from django.conf import settings
from django.core.cache import caches
from django.db import models
from django.utils.text import slugify

from seevr.live.app import caching

cache = caches[settings.SESSION_CACHE_ALIAS]


class Feature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", max_length=100, editable=False)
    turn_duration = models.DurationField(default=timedelta(minutes=2))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def _key_prefix(self):
        return f"{self.pk}:{self.slug}:"

    @property
    def guest_queue(self):
        return caching.CachedListSet(key=self._key_prefix + "guest_queue")

    @property
    def member_channels(self):
        return caching.CachedListSet(self._key_prefix + "member_channels")

    @property
    def presenter_channel(self):
        return cache.get(self._key_prefix + "presenter_channel")

    @presenter_channel.setter
    def presenter_channel(self, value):
        return cache.set(self._key_prefix + "presenter_channel", value)


class Guest(models.Model):
    name = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100, primary_key=True)
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="features"
    )

    def __str__(self):
        return self.name
