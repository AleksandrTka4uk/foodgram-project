from django.contrib import admin
from apps.recipes.models import Ingredient, Tag, Recipe, RecipeIngredient, Favorite, Subscription, Purchase


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)

class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Purchase)
