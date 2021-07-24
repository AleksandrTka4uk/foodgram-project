from django.urls import path

from apps.about.views import AboutView, TechView

urlpatterns = [
    path('author/', AboutView.as_view(), name='about'),
    path('tech/', TechView.as_view(), name='tech')
]
