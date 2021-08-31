from django.contrib import admin
from django.db.models import Count


from apps.recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                                 RecipeIngredient, Subscription, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'tag_display', 'in_favorite_count', )
    list_filter = ('tag',)
    search_fields = ['title']
    readonly_fields = ('in_favorite_count',)
    list_per_page = 25

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _in_favorites_count=Count('in_favorites', distinct=True),
        )
        return queryset

    @admin.display(description='Количество в избранном')
    def in_favorite_count(self, obj):
        return obj._in_favorites_count

    @admin.display(description='Теги')
    def tag_display(self, obj):
        return ", ".join([tag.title for tag in obj.tag.all()])

    in_favorite_count.admin_order_field = '_in_favorites_count'


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'in_favorite_count')
    search_fields = ['title']
    readonly_fields = ('in_favorite_count',)
    list_per_page = 25

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _in_favorites_count=Count('in_recipes__recipe__in_favorites',
                                      distinct=True),
        )
        return queryset

    @admin.display(description='Количество в избранном')
    def in_favorite_count(self, obj):
        return obj._in_favorites_count

    in_favorite_count.admin_order_field = '_in_favorites_count'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Purchase)
admin.site.register(RecipeIngredient)
