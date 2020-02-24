from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))
