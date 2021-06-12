from django.views.generic.base import TemplateView

class AboutView(TemplateView):
    template_name = 'AboutPage.html'


class TechView(TemplateView):
    template_name = 'TechPage.html'
