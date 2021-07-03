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
def tag_in_tags_off(tag_id, request):
    return tag_id in request.GET.getlist('tags_off')


@register.simple_tag
def add_to_tags_off(tag_id, request):
    request_copy = request.GET.copy()
    request_copy.__setitem__('page', 1)
    tags_off = request_copy.getlist('tags_off')
    if tags_off:
        request_copy.appendlist('tags_off', tag_id)
    else:
        request_copy.setlist('tags_off', tag_id)
    return request_copy.urlencode()


@register.simple_tag
def remove_from_tags_off(tag_id, request):
    request_copy = request.GET.copy()
    tags_off = request_copy.getlist('tags_off')
    tags_off.remove(tag_id)
    request_copy.setlist('tags_off', tags_off)
    return request_copy.urlencode()


@register.simple_tag
def tags_off_params(request):
    request_copy = request.GET.copy()
    if request_copy.getlist('page'):
        request_copy.pop('page')
    return request_copy.urlencode()


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
