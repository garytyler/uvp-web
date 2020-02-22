from django.views.generic.base import TemplateView


class IndexTemplateView(TemplateView):
    def get_template_names(self):
        # if settings.DEBUG:
        #     template_name = "index-dev.html"
        # else:
        #     template_name = "index.html"
        # return template_name
        return "index.html"