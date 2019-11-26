from django.contrib import admin

from .models import Feature

admin.site.register(Feature)


class FeatureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
