from random import choices, randint

from django.core.management.base import BaseCommand

from apps.recipes.factories import RecipeFactory
from apps.recipes.models import Tag
from apps.users.factories import UserFactory

USERS = 10
MAX_RECIPES = 10
MAX_FAVORITES = 4


class Command(BaseCommand):
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(USERS)

        tags = Tag.objects.all()

        for user in users:
            for _ in range(randint(0, MAX_RECIPES)):
                RecipeFactory(author=user, tag=choices(tags, k=2))
