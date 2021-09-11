from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = 'about/AboutPage.html'


class TechView(TemplateView):
    template_name = 'about/TechPage.html'
