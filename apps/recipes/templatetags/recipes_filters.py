from django import template

from apps.recipes.models import Tag

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def is_signed_to_author(author, user):
    return user.subscriptions.filter(author=author).exists()


@register.simple_tag
def tag_in_recipe(recipe, tag_title):
    return recipe.tag.filter(title=tag_title).exists()


@register.simple_tag
def recipes_format_text(recipes_count):
    remainder = recipes_count % 10
    if remainder == 0 or remainder >= 5 or (10 <= recipes_count <= 19):
        return f'{recipes_count} рецептов'
    elif remainder == 1:
        return f'{recipes_count} рецепт'
    else:
        return f'{recipes_count} рецепта'
