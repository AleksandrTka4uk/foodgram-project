import csv

from django.core.management.base import BaseCommand

from apps.recipes.models import Tag


class Command(BaseCommand):
    help = 'Import data from tags.csv'

    def handle(self, *args, **options):
        with open('tags.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                title, color, slug = row
                Tag.objects.get_or_create(title=title,
                                          color=color,
                                          slug=slug,
                                          )
