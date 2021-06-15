from django.contrib import admin
from apps.recipes.models import Ingredient, Tag, Recipe, RecipeIngredient, Favorite, Subscription, Purchase
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
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
