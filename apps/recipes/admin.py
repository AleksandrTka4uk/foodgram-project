from django.contrib import admin
from apps.recipes.models import Ingredient, Tag, Recipe


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)

