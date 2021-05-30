from django import template


register = template.Library()


@register.simple_tag
def is_favorite_tag(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()
