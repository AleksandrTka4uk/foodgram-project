from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                                 RecipeIngredient, Subscription, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_filter = ('title',)
    search_fields = ['title']


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_filter = ('title',)
    search_fields = ['title']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Purchase)
admin.site.register(RecipeIngredient)
