from django.contrib import admin

from .models import Feature, Guest

# class FeatureAdmin(admin.ModelAdmin):
#     pass
#     # prepopulated_fields = {"slug": ("title",)}


admin.site.register(Feature)
admin.site.register(Guest)
