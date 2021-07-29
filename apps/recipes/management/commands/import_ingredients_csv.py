import csv

from django.core.management.base import BaseCommand

from apps.recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from ingredients.csv'

    def handle(self, *args, **options):
        with open('ingredients.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                title, dimension = row
                Ingredient.objects.get_or_create(title=title, dimension=measure)
